## alibaba user behavior dataset
UserBehavior是阿里巴巴提供的一个淘宝用户行为数据集，用于隐式反馈推荐问题的研究。

时间: 2017年11月25日-2017年12月3日.

组织形式: 类似MovieLens-20M, 即每一行表示一条用户行为，由用户ID、商品ID、商品类目ID、行为类型和时间戳组成，并以逗号分隔。

## description
|列说明|说明|规模|
|----|----|----|
|用户ID|整数类型，序列化后的用户ID|987,994|
|商品ID|整数类型，序列化后的商品ID|4,162,024|
|商品类目ID|整数类型，序列化后的商品所属类目ID|9,439|
|行为类型|字符串枚举类型，包括('pv', 'buy', 'cart', 'fav')|100,150,807|

行为类型
1. pv	商品详情页pv，等价于点击
2. buy	商品购买
3. cart	将商品加入购物车
4. fav	收藏商品关于数据集大小的一些说明如下

## 论文引用
1. Han Z, Xiang L, Pengye Z, et al. Learning Tree-based Deep Model for Recommender Systems. In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining.
2. Han Z, Daqing C, Ziru X, et al. Joint Optimization of Tree-based Index and Deep Model for Recommender Systems. arXiv:1902.07565.