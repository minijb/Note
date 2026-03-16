---
tags:
  - raytrace
---
## 8 Antialiasing


如何 采样？

采样以像素为中心的正方形区域，该区域延伸到四个相邻像素中的每个像素的一半。

### 使用随机数

```cpp
#include <cstdlib>

inline double random_double() {
    // Returns a random real in [0,1).
    return rand() / (RAND_MAX + 1.0);
}

inline double random_double(double min, double max) {
    // Returns a random real in [min,max).
    return min + (max-min)*random_double();
}
```


修改一下 color.h

```cpp
#include "interval.h"
#include "vec3.h"

using color = vec3;

void write_color(std::ostream& out, const color& pixel_color) {
    auto r = pixel_color.x();
    auto g = pixel_color.y();
    auto b = pixel_color.z();

    // Translate the [0,1] component values to the byte range [0,255].
    static const interval intensity(0.000, 0.999);
    int rbyte = int(256 * intensity.clamp(r));
    int gbyte = int(256 * intensity.clamp(g));
    int bbyte = int(256 * intensity.clamp(b));

    // Write out the pixel color components.
    out << rbyte << ' ' << gbyte << ' ' << bbyte << '\n';
}
```

修改 camera

```cpp
class camera {
  public:
    double aspect_ratio      = 1.0;  // Ratio of image width over height
    int    image_width       = 100;  // Rendered image width in pixel count
    int    samples_per_pixel = 10;   // Count of random samples for each pixel

    void render(const hittable& world) {
        initialize();

        std::cout << "P3\n" << image_width << ' ' << image_height << "\n255\n";

        for (int j = 0; j < image_height; j++) {
            std::clog << "\rScanlines remaining: " << (image_height - j) << ' ' << std::flush;
            for (int i = 0; i < image_width; i++) {
                color pixel_color(0,0,0);
                for (int sample = 0; sample < samples_per_pixel; sample++) {
                    ray r = get_ray(i, j);
                    pixel_color += ray_color(r, world);
                }
                write_color(std::cout, pixel_samples_scale * pixel_color);
            }
        }

        std::clog << "\rDone.                 \n";
    }
    ...
  private:
    int    image_height;         // Rendered image height
    double pixel_samples_scale;  // Color scale factor for a sum of pixel samples
    point3 center;               // Camera center
    point3 pixel00_loc;          // Location of pixel 0, 0
    vec3   pixel_delta_u;        // Offset to pixel to the right
    vec3   pixel_delta_v;        // Offset to pixel below

    void initialize() {
        image_height = int(image_width / aspect_ratio);
        image_height = (image_height < 1) ? 1 : image_height;

        pixel_samples_scale = 1.0 / samples_per_pixel;

        center = point3(0, 0, 0);
        ...
    }

    ray get_ray(int i, int j) const {
        // Construct a camera ray originating from the origin and directed at randomly sampled
        // point around the pixel location i, j.

        auto offset = sample_square();
        auto pixel_sample = pixel00_loc
                          + ((i + offset.x()) * pixel_delta_u)
                          + ((j + offset.y()) * pixel_delta_v);

        auto ray_origin = center;
        auto ray_direction = pixel_sample - ray_origin;

        return ray(ray_origin, ray_direction);
    }

    vec3 sample_square() const {
        // Returns the vector to a random point in the [-.5,-.5]-[+.5,+.5] unit square.
        return vec3(random_double() - 0.5, random_double() - 0.5, 0);
    }

    color ray_color(const ray& r, const hittable& world) const {
        ...
    }
};

#endif
```


总结

- samples_per_pixel ： 10 在一定范围内随机射出10个 ray 并计算平均值 以此来模糊边界。

## 漫反射材质

- 不发光但是吸收光线
- 会随机反射光线

![400](https://raytracing.github.io/images/fig-1.09-light-bounce.jpg)


- 越黑 --- 吸收的光线越多。
- 反射的方向完全随机

![400](https://raytracing.github.io/images/fig-1.10-random-vec-horizon.jpg)



为 vec3 添加 随机散射的效果

```cpp
class vec3 {
  public:
    ...

    double length_squared() const {
        return e[0]*e[0] + e[1]*e[1] + e[2]*e[2];
    }

    static vec3 random() {
        return vec3(random_double(), random_double(), random_double());
    }

    static vec3 random(double min, double max) {
        return vec3(random_double(min,max), random_double(min,max), random_double(min,max));
    }
```


通过 拒绝的方法 产生 只发生半球范围的随机散射

> 拒绝的方法 ： 不断尝试知道符合要求

1. nerate a random vector inside of the unit sphere
2. Normalize this vector
3. Invert the normalized vector if it falls onto the wrong hemisphere

**1：得到一个随机的球内的方向**

```cpp
inline vec3 random_in_unit_sphere() {
    while (true) {
        auto p = vec3::random(-1,1);
        if (p.length_squared() < 1)
            return p;
    }
}
```

**2： 标准化**

```cpp
inline vec3 random_unit_vector() {
    return unit_vector(random_in_unit_sphere());
}
```

**3： 确定是否在对的半球上**

- 如果和法线 角度小于90 则正确，否则则反向

```cpp
inline vec3 random_on_hemisphere(const vec3& normal) {
    vec3 on_unit_sphere = random_unit_vector();
    if (dot(on_unit_sphere, normal) > 0.0) // In the same hemisphere as the normal
        return on_unit_sphere;
    else
        return -on_unit_sphere;
}
```


一般来说如果是白色，返回全部光，如果是黑色则吸收光，这里我们全部取 50

```cpp
class camera {
  ...
  private:
    ...
    color ray_color(const ray& r, const hittable& world) const {
        hit_record rec;

        if (world.hit(r, interval(0, infinity), rec)) {
            vec3 direction = random_on_hemisphere(rec.normal);
            return 0.5 * ray_color(ray(rec.p, direction), world);
        }

        vec3 unit_direction = unit_vector(r.direction());
        auto a = 0.5*(unit_direction.y() + 1.0);
        return (1.0-a)*color(1.0, 1.0, 1.0) + a*color(0.5, 0.7, 1.0);
    }
};
```


### 限制 子射线的次数

这里潜伏着一个潜在的问题。注意，光线颜色函数是递归的。它什么时候会停止递归?当它没有击中任何东西的时候。然而，在某些情况下，这可能是足够长的时间来炸毁堆栈。为了防止这种情况，让我们限制最大递归深度，在最大深度不返回任何光贡献。


```cpp
class camera {
  public:
    double aspect_ratio      = 1.0;  // Ratio of image width over height
    int    image_width       = 100;  // Rendered image width in pixel count
    int    samples_per_pixel = 10;   // Count of random samples for each pixel
    int    max_depth         = 10;   // Maximum number of ray bounces into scene

    void render(const hittable& world) {
        initialize();

        std::cout << "P3\n" << image_width << ' ' << image_height << "\n255\n";

        for (int j = 0; j < image_height; j++) {
            std::clog << "\rScanlines remaining: " << (image_height - j) << ' ' << std::flush;
            for (int i = 0; i < image_width; i++) {
                color pixel_color(0,0,0);
                for (int sample = 0; sample < samples_per_pixel; sample++) {
                    ray r = get_ray(i, j);
                    pixel_color += ray_color(r, max_depth, world);
                }
                write_color(std::cout, pixel_samples_scale * pixel_color);
            }
        }

        std::clog << "\rDone.                 \n";
    }
    ...
  private:
    ...
    color ray_color(const ray& r, int depth, const hittable& world) const {
        // If we've exceeded the ray bounce limit, no more light is gathered.
        if (depth <= 0)
            return color(0,0,0);

        hit_record rec;

        if (world.hit(r, interval(0, infinity), rec)) {
            vec3 direction = random_on_hemisphere(rec.normal);
            return 0.5 * ray_color(ray(rec.p, direction), depth-1, world);
        }

        vec3 unit_direction = unit_vector(r.direction());
        auto a = 0.5*(unit_direction.y() + 1.0);
        return (1.0-a)*color(1.0, 1.0, 1.0) + a*color(0.5, 0.7, 1.0);
    }
};
```

### Fixing Shadow Acne

当射线与一个表面相交时，它会试图精确地计算交点.不幸的是，对于我们来说，这种计算容易受到浮点舍入误差的影响，这可能导致交点稍微偏离. 会出现在平面上或者下。如果射线的原点在表面的下方那么它可以再次与表面相交。解决这一问题的最简单方法是忽略那些非常接近计算交叉点的命中。

```cpp
class camera {
  ...
  private:
    ...
    color ray_color(const ray& r, int depth, const hittable& world) const {
        // If we've exceeded the ray bounce limit, no more light is gathered.
        if (depth <= 0)
            return color(0,0,0);

        hit_record rec;

        if (world.hit(r, interval(0.001, infinity), rec)) { //!!!!!!!!!!!!!
            vec3 direction = random_on_hemisphere(rec.normal);
            return 0.5 * ray_color(ray(rec.p, direction), depth-1, world);
        }

        vec3 unit_direction = unit_vector(r.direction());
        auto a = 0.5*(unit_direction.y() + 1.0);
        return (1.0-a)*color(1.0, 1.0, 1.0) + a*color(0.5, 0.7, 1.0);
    }
};
```

**稍微亮一点**

### True Lambertian Reflection

分布和 $\cos{\theta}$ 成正比

这意味着反射的光线最有可能在接近表面法线的方向上散射，而不太可能在远离法线的方向上散射。这种非均匀的朗伯分布比我们之前的均匀散射更好地模拟了现实世界中的材料反射。

我们可以通过在法向量上添加一个随机单位向量来创建这个分布。在交点处，这个曲面正好有两条边，所以只能有两个唯一的单位球与任何交点相切(曲面的每条边都有一个唯一的球)。这两个单位球将会从表面位移出它们的半径长度，对于单位球来说正好是1。

![400](https://raytracing.github.io/images/fig-1.14-rand-unitvec.jpg)


此时有两个球体, 一个以 $P+n$ 为圆心，在表面外侧 ， 一个以 $P-n$ 在表面内测

在这个圆上随机选一个点 S ，反射的光线就是 $S-P$

```cpp
class camera {
    ...
    color ray_color(const ray& r, int depth, const hittable& world) const {
        // If we've exceeded the ray bounce limit, no more light is gathered.
        if (depth <= 0)
            return color(0,0,0);

        hit_record rec;

        if (world.hit(r, interval(0.001, infinity), rec)) {
            vec3 direction = rec.normal + random_unit_vector();
            return 0.5 * ray_color(ray(rec.p, direction), depth-1, world);
        }

        vec3 unit_direction = unit_vector(r.direction());
        auto a = 0.5*(unit_direction.y() + 1.0);
        return (1.0-a)*color(1.0, 1.0, 1.0) + a*color(0.5, 0.7, 1.0);
    }
};
```

### 使用伽玛校正准确的色彩强度

注意球体下的阴影。图片很暗，但我们的球体只吸收了每次反弹的一半能量，所以它们是50%的反射器。这些球体看起来应该很亮(在现实生活中，是浅灰色)，但它们看起来相当暗。如果我们通过漫射材料的全亮度范围，我们可以更清楚地看到这一点。我们首先设置光线颜色函数的反射率从0.5(50%)到0.1(10%)。

我们江数据存储到 gamma 空间。使用 gamma 2 变换。 --- $\frac{1}{\gamma}$ 也就是平方根

```cpp
inline double linear_to_gamma(double linear_component)
{
    if (linear_component > 0)
        return sqrt(linear_component);

    return 0;
}

void write_color(std::ostream& out, const color& pixel_color) {
    auto r = pixel_color.x();
    auto g = pixel_color.y();
    auto b = pixel_color.z();

    // Apply a linear to gamma transform for gamma 2
    r = linear_to_gamma(r);
    g = linear_to_gamma(g);
    b = linear_to_gamma(b);

    // Translate the [0,1] component values to the byte range [0,255].
    static const interval intensity(0.000, 0.999);
    int rbyte = int(256 * intensity.clamp(r));
    int gbyte = int(256 * intensity.clamp(g));
    int bbyte = int(256 * intensity.clamp(b));

    // Write out the pixel color components.
    out << rbyte << ' ' << gbyte << ' ' << bbyte << '\n';
}
```

此时，从明亮到黑暗 更加平滑。

