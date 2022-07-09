- 计算出步长

```python
    stride_h = self.input_shape[0] / in_h
    stride_w = self.input_shape[1] / in_w
```

416/13=32也就是说那个grid ceil有32*32个像素

- 用先验框的宽高除以步长，得到先验框相对于特征层的大小！！！

```python
scaled_anchors  = [(a_w / stride_w, a_h / stride_h) for a_w, a_h in self.anchors]
```

- 调整预测的输出的通道,方便之后计算

`bs,3*(5+classes),13,13`==>`bs,3,13,13,5+classes`

```python
prediction = input.view(bs, len(self.anchors_mask[l]), self.bbox_attrs, in_h, in_w).permute(0, 1, 3, 4, 2).contiguous()
```

- 得到各个部分的数值

```python
#-----------------------------------------------#
#   先验框的中心位置的调整参数
#-----------------------------------------------#
x = torch.sigmoid(prediction[..., 0])
y = torch.sigmoid(prediction[..., 1])
#-----------------------------------------------#
#   先验框的宽高调整参数
#-----------------------------------------------#
w = prediction[..., 2]
h = prediction[..., 3]
#-----------------------------------------------#
#   获得置信度，是否有物体
#-----------------------------------------------#
conf = torch.sigmoid(prediction[..., 4])
#-----------------------------------------------#
#   种类置信度
#-----------------------------------------------#
pred_cls = torch.sigmoid(prediction[..., 5:])

#-----------------------------------------------#
#   获得网络应该有的预测结果
#-----------------------------------------------#
y_true, noobj_mask, box_loss_scale = self.get_target(l, targets, scaled_anchors, in_h, in_w)

```

- 获得当前网格应该有的数据

```python
def get_target(self, l, targets, anchors, in_h, in_w):
    #-----------------------------------------------------#
    #   计算一共有多少张图片
    #-----------------------------------------------------#
    bs              = len(targets)
    #-----------------------------------------------------#
    #   用于选取哪些先验框不包含物体
    #-----------------------------------------------------#
    noobj_mask      = torch.ones(bs, len(self.anchors_mask[l]), in_h, in_w, requires_grad = False)
    #-----------------------------------------------------#
    #   让网络更加去关注小目标
    #-----------------------------------------------------#
    box_loss_scale  = torch.zeros(bs, len(self.anchors_mask[l]), in_h, in_w, requires_grad = False)
    #-----------------------------------------------------#
    #   batch_size, 3, 13, 13, 5 + num_classes
    #-----------------------------------------------------#
    y_true          = torch.zeros(bs, len(self.anchors_mask[l]), in_h, in_w, self.bbox_attrs, requires_grad = False)
    for b in range(bs):            
        if len(targets[b])==0:
            continue
        batch_target = torch.zeros_like(targets[b])
        #-------------------------------------------------------#
        #   计算出正样本在特征层上的中心点
        #-------------------------------------------------------#
        batch_target[:, [0,2]] = targets[b][:, [0,2]] * in_w
        batch_target[:, [1,3]] = targets[b][:, [1,3]] * in_h
        batch_target[:, 4] = targets[b][:, 4]
        batch_target = batch_target.cpu()

        #-------------------------------------------------------#
        #   将真实框转换一个形式
        #   num_true_box, 4
        #-------------------------------------------------------#
        gt_box  =torch.FloatTensor(torch.cat((torch.zeros((batch_target.size(0), 2)), batch_target[:, 2:4]), 1))
        #-------------------------------------------------------#
        #   将先验框转换一个形式
        #   9, 4
        #-------------------------------------------------------#
        anchor_shapes   = torch.FloatTensor(torch.cat((torch.zeros((len(anchors), 2)), torch.FloatTensor(anchors)), 1))
        #-------------------------------------------------------#
        #   计算交并比
        #   self.calculate_iou(gt_box, anchor_shapes) = [num_true_box, 9]每一个真实框和9个先验框的重合情况
        #   best_ns:
        #   [每个真实框最大的重合度max_iou, 每一个真实框最重合的先验框的序号]
        #-------------------------------------------------------#
        best_ns = torch.argmax(self.calculate_iou(gt_box, anchor_shapes), dim=-1)

        for t, best_n in enumerate(best_ns):
            if best_n not in self.anchors_mask[l]:
                continue
            #----------------------------------------#
            #   判断这个先验框是当前特征点的哪一个先验框
            #----------------------------------------#
            k = self.anchors_mask[l].index(best_n)
            #----------------------------------------#
            #   获得真实框属于哪个网格点
            #----------------------------------------#
            i = torch.floor(batch_target[t, 0]).long()
            j = torch.floor(batch_target[t, 1]).long()
            #----------------------------------------#
            #   取出真实框的种类
            #----------------------------------------#
            c = batch_target[t, 4].long()

            #----------------------------------------#
            #   noobj_mask代表无目标的特征点
            #----------------------------------------#
            noobj_mask[b, k, j, i] = 0
            #----------------------------------------#
            #   tx、ty代表中心调整参数的真实值
            #----------------------------------------#
            y_true[b, k, j, i, 0] = batch_target[t, 0]
            y_true[b, k, j, i, 1] = batch_target[t, 1]
            y_true[b, k, j, i, 2] = batch_target[t, 2]
            y_true[b, k, j, i, 3] = batch_target[t, 3]
            y_true[b, k, j, i, 4] = 1
            y_true[b, k, j, i, c + 5] = 1
            #----------------------------------------#
            #   用于获得xywh的比例
            #   大目标loss权重小，小目标loss权重大
            #----------------------------------------#
            box_loss_scale[b, k, j, i] = batch_target[t, 2] * batch_target[t, 3] / in_w / in_h
            return y_true, noobj_mask, box_loss_scale
```

他会选取包含和不包含物体的anchor，得出y_true应该输出的结果

box_loss_scale的作用是，让大目标的权值小一些，小目标的全职大一些

- 解码过程(解码预测的过程)

```python
def get_ignore(self, l, x, y, h, w, targets, scaled_anchors, in_h, in_w, noobj_mask):
    #-----------------------------------------------------#
    #   计算一共有多少张图片
    #-----------------------------------------------------#
    bs = len(targets)

    #-----------------------------------------------------#
    #   生成网格，先验框中心，网格左上角
    #-----------------------------------------------------#
    grid_x = torch.linspace(0, in_w - 1, in_w).repeat(in_h, 1).repeat(
        int(bs * len(self.anchors_mask[l])), 1, 1).view(x.shape).type_as(x)
    grid_y = torch.linspace(0, in_h - 1, in_h).repeat(in_w, 1).t().repeat(
        int(bs * len(self.anchors_mask[l])), 1, 1).view(y.shape).type_as(x)

    # 生成先验框的宽高
    scaled_anchors_l = np.array(scaled_anchors)[self.anchors_mask[l]]
    anchor_w = torch.Tensor(scaled_anchors_l).index_select(1, torch.LongTensor([0])).type_as(x)
    anchor_h = torch.Tensor(scaled_anchors_l).index_select(1, torch.LongTensor([1])).type_as(x)

    anchor_w = anchor_w.repeat(bs, 1).repeat(1, 1, in_h * in_w).view(w.shape)
    anchor_h = anchor_h.repeat(bs, 1).repeat(1, 1, in_h * in_w).view(h.shape)
    #-------------------------------------------------------#
    #   计算调整后的先验框中心与宽高
    #-------------------------------------------------------#
    pred_boxes_x    = torch.unsqueeze(x + grid_x, -1)
    pred_boxes_y    = torch.unsqueeze(y + grid_y, -1)
    pred_boxes_w    = torch.unsqueeze(torch.exp(w) * anchor_w, -1)
    pred_boxes_h    = torch.unsqueeze(torch.exp(h) * anchor_h, -1)
    pred_boxes      = torch.cat([pred_boxes_x, pred_boxes_y, pred_boxes_w, pred_boxes_h], dim = -1)

    for b in range(bs):           
        #-------------------------------------------------------#
        #   将预测结果转换一个形式
        #   pred_boxes_for_ignore      num_anchors, 4
        #-------------------------------------------------------#
        pred_boxes_for_ignore = pred_boxes[b].view(-1, 4)
        #-------------------------------------------------------#
        #   计算真实框，并把真实框转换成相对于特征层的大小
        #   gt_box      num_true_box, 4
        #-------------------------------------------------------#
        if len(targets[b]) > 0:
            batch_target = torch.zeros_like(targets[b])
            #-------------------------------------------------------#
            #   计算出正样本在特征层上的中心点
            #-------------------------------------------------------#
            batch_target[:, [0,2]] = targets[b][:, [0,2]] * in_w
            batch_target[:, [1,3]] = targets[b][:, [1,3]] * in_h
            batch_target = batch_target[:, :4].type_as(x)
            #-------------------------------------------------------#
            #   计算交并比
            #   anch_ious       num_true_box, num_anchors
            #-------------------------------------------------------#
            anch_ious = self.calculate_iou(batch_target, pred_boxes_for_ignore)
            #-------------------------------------------------------#
            #   每个先验框对应真实框的最大重合度
            #   anch_ious_max   num_anchors
            #-------------------------------------------------------#
            anch_ious_max, _    = torch.max(anch_ious, dim = 0)
            anch_ious_max       = anch_ious_max.view(pred_boxes[b].size()[:3])
            noobj_mask[b][anch_ious_max > self.ignore_threshold] = 0
            return noobj_mask, pred_boxes

```

- 利用预测结果和真实框计算CIOU，并计算损失

```python
if n != 0:
    #---------------------------------------------------------------#
    #   计算预测结果和真实结果的差距
    #   loss_loc iou回归损失
    #   loss_cls 分类损失
    #---------------------------------------------------------------#
    iou         = self.box_iou(pred_boxes, y_true[..., :4]).type_as(x)
    obj_mask    = obj_mask & torch.logical_not(torch.isnan(iou))
    loss_loc    = torch.mean((1 - iou)[obj_mask])
    # loss_loc    = torch.mean((1 - iou)[obj_mask] * box_loss_scale[obj_mask])

    loss_cls    = torch.mean(self.BCELoss(pred_cls[obj_mask], y_true[..., 5:][obj_mask]))
    loss        += loss_loc * self.box_ratio + loss_cls * self.cls_ratio

    #---------------------------------------------------------------#
    #   计算是否包含物体的置信度损失
    #---------------------------------------------------------------#
    if self.focal_loss:
        pos_neg_ratio   = torch.where(obj_mask, torch.ones_like(conf) * self.alpha, torch.ones_like(conf) * (1 - self.alpha)) 
        hard_easy_ratio = torch.where(obj_mask, torch.ones_like(conf) - conf, conf) ** self.gamma
        loss_conf   = torch.mean((self.BCELoss(conf, obj_mask.type_as(conf)) * pos_neg_ratio * hard_easy_ratio)[noobj_mask.bool() | obj_mask]) * self.focal_loss_ratio
    else: 
        loss_conf   = torch.mean(self.BCELoss(conf, obj_mask.type_as(conf))[noobj_mask.bool() | obj_mask])
        loss        += loss_conf * self.balance[l] * self.obj_ratio
        # if n != 0:
        #     print(loss_loc * self.box_ratio, loss_cls * self.cls_ratio, loss_conf * self.balance[l] * self.obj_ratio)
        return loss
```



