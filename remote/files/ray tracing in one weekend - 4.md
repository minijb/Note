---
tags:
  - raytrace
---
## Metal

对材质进行抽象

- 产生散射射线(或者说吸收入射射线)。
- 如果散射，说明射线应该衰减多少。

```cpp
#ifndef MATERIAL_H
#define MATERIAL_H

#include "rtweekend.h"

class hit_record;

class material {
  public:
    virtual ~material() = default;

    virtual bool scatter(
        const ray& r_in, const hit_record& rec, color& attenuation, ray& scattered
    ) const {
        return false;
    }
};

#endif
```


### 描述光线与物体相交的数据结构

hit record是为了避免一堆参数这样我们就可以把任何想要的信息塞进去。您可以使用参数而不是封装类型，这只是个人喜好问题。Hittables和材料需要能够在代码中引用对方的类型，所以引用有一些循环性。在c++中，我们添加了行类材料;告诉编译器material是一个稍后将定义的类。由于我们只是指定了一个指向类的指针，编译器不需要知道类的细节，从而解决了循环引用问题。

- 使用指针解决循环问题

```cpp
class material;

class hit_record {
  public:
    point3 p;
    vec3 normal;
    shared_ptr<material> mat; //！！！！！！！！！！！
    double t;
    bool front_face;

    void set_face_normal(const ray& r, const vec3& outward_normal) {
        front_face = dot(r.direction(), outward_normal) < 0;
        normal = front_face ? outward_normal : -outward_normal;
    }
};
```


一旦光线接触到某个平面，那么 `hit_record` 就会set the point of matel。当使用 ray color 的时候，，它可以调用材质指针的成员函数来查找散射的光线(如果有)。

```cpp
class sphere : public hittable {
  public:
    sphere(const point3& center, double radius) : center(center), radius(fmax(0,radius)) {
        // TODO: Initialize the material pointer `mat`.
    }

    bool hit(const ray& r, interval ray_t, hit_record& rec) const override {
        ...

        rec.t = root;
        rec.p = r.at(rec.t);
        vec3 outward_normal = (rec.p - center) / radius;
        rec.set_face_normal(r, outward_normal);
        rec.mat = mat;

        return true;
    }

  private:
    point3 center;
    double radius;
    shared_ptr<material> mat;
};
```

> 简单流程：render : hit 击中，记录材质 法线。。。。 保存在 hit_record
> 				计算颜色，进行递归。


### Light Scatter and Reflectance

反照率会随着材料颜色的变化而变化(我们稍后会在玻璃材料中实现)，也会随着入射观察方向(入射光线的方向)而变化。

根据反射率 R 进行反射或折射， 1-R 进行散射， 如果不散射就吸收光线。
实现 Lambertian 材质

```cpp
class material {
    ...
};

class lambertian : public material {
  public:
    lambertian(const color& albedo) : albedo(albedo) {}

    bool scatter(const ray& r_in, const hit_record& rec, color& attenuation, ray& scattered)
    const override {
        auto scatter_direction = rec.normal + random_unit_vector();
        scattered = ray(rec.p, scatter_direction);
        attenuation = albedo;
        return true;
    }

  private:
    color albedo;
};
```

**attenuation** : 反射率。

如果我们生成的随机单位向量正好与法向量相反，则两者之和为零，这将导致零散射方向向量。这将导致稍后出现糟糕的情况(无穷大和nan)，因此我们需要在传递条件之前拦截它。

```cpp
// rtweekend

// C++ Std Usings

using std::fabs;
using std::make_shared;
using std::shared_ptr;
using std::sqrt;


// vec3

class vec3 {
    ...

    double length_squared() const {
        return e[0]*e[0] + e[1]*e[1] + e[2]*e[2];
    }

    bool near_zero() const {
        // Return true if the vector is close to zero in all dimensions.
        auto s = 1e-8;
        return (fabs(e[0]) < s) && (fabs(e[1]) < s) && (fabs(e[2]) < s);
    }

    ...
};

//material
class lambertian : public material {
  public:
    lambertian(const color& albedo) : albedo(albedo) {}

    bool scatter(const ray& r_in, const hit_record& rec, color& attenuation, ray& scattered)
    const override {
        auto scatter_direction = rec.normal + random_unit_vector();

        // Catch degenerate scatter direction
        if (scatter_direction.near_zero())
            scatter_direction = rec.normal;

        scattered = ray(rec.p, scatter_direction);
        attenuation = albedo;
        return true;
    }

  private:
    color albedo;
};
```

### Mirrored Light Reflection

对于抛光金属，光线不会随机散射。关键问题是:光线是如何从金属镜子反射回来的?向量数学是我们的朋友

![400](https://raytracing.github.io/images/fig-1.15-reflection.jpg)


反射光线(红) : $v+2b$ 。n: 单位向量， v不是。如何得到b呢

b 的长度 : 就是 v 在 n 上的 投影。 --- $v \cdot n$  由于方向指向 表面内， 因此 长度需要取负值。

```cpp
inline vec3 reflect(const vec3& v, const vec3& n) {
    return v - 2*dot(v,n)*n;
}
```

金属材质

```cpp
class lambertian : public material {
    ...
};

class metal : public material {
  public:
    metal(const color& albedo) : albedo(albedo) {}

    bool scatter(const ray& r_in, const hit_record& rec, color& attenuation, ray& scattered)
    const override {
        vec3 reflected = reflect(r_in.direction(), rec.normal);
        scattered = ray(rec.p, reflected);
        attenuation = albedo;
        return true;
    }

  private:
    color albedo;
};
```

此时 ray_color 就是 

```cpp
...
#include "rtweekend.h"

#include "hittable.h"
#include "material.h"
...

class camera {
  ...
  private:
    ...
    color ray_color(const ray& r, int depth, const hittable& world) const {
        // If we've exceeded the ray bounce limit, no more light is gathered.
        if (depth <= 0)
            return color(0,0,0);

        hit_record rec;

        if (world.hit(r, interval(0.001, infinity), rec)) {
            ray scattered;
            color attenuation;
            // 这里 集中物体，检查材质并 散射。 根据 材质的 吸收的反射率 计算颜色
            if (rec.mat->scatter(r, rec, attenuation, scattered))
                return attenuation * ray_color(scattered, depth-1, world);
            return color(0,0,0);
        }

        vec3 unit_direction = unit_vector(r.direction());
        auto a = 0.5*(unit_direction.y() + 1.0);
        return (1.0-a)*color(1.0, 1.0, 1.0) + a*color(0.5, 0.7, 1.0);
    }
};
```


### 模糊的反射

我们也可以通过使用一个小球体并为光线选择一个新的端点来随机化反射方向。我们将使用以原始端点为中心的球体表面的随机点，通过模糊因子缩放。

![400](https://raytracing.github.io/images/fig-1.16-reflect-fuzzy.jpg)


模糊球越大，反射越模糊。这建议添加一个模糊参数，即球体的半径(因此零表示没有扰动)。问题是，对于大的球体或掠射射线，我们可能会在地表以下散射。我们可以让表面吸收这些。

The bigger the fuzz sphere, the fuzzier the reflections will be. This suggests adding a fuzziness parameter that is just the radius of the sphere (so zero is no perturbation). The catch is that for big spheres or grazing rays, we may scatter below the surface. We can just have the surface absorb those.

还要注意，为了使模糊球有意义，它需要与反射向量保持一致的比例，反射向量的长度可以任意变化。为了解决这个问题，我们需要将反射光线归一化。

```cpp
class metal : public material {
  public:
  // fuzz 不能 大于 1
    metal(const color& albedo, double fuzz) : albedo(albedo), fuzz(fuzz < 1 ? fuzz : 1) {}

    bool scatter(const ray& r_in, const hit_record& rec, color& attenuation, ray& scattered)
    const override {
        vec3 reflected = reflect(r_in.direction(), rec.normal);
        reflected = unit_vector(reflected) + (fuzz * random_unit_vector());
        scattered = ray(rec.p, reflected);
        attenuation = albedo;
        // 防止 模糊之后 的散射 衍生到平面之下
        return (dot(scattered.direction(), rec.normal) > 0);
    }

  private:
    color albedo;
    double fuzz;
};
```