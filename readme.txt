//实现部分api接口
1.
http://moonmonsters.pythonanywhere.com/api/hotblog/?type=*
type = 0 时返回今日热门博客
type = 1 时返回昨日热门博客
type = 2时返回前10日热门博客
type = 3时返回前1个月热门博客

2.
http://moonmonsters.pythonanywhere.com/api/blogdetail/?pk=?
根据pk值查询某篇博客具体内容

3.
http://moonmonsters.pythonanywhere.com/api/newcommentcount/
返回用户新增加评论数量，在右上角显示

4.
http://moonmonsters.pythonanywhere.com/api/newcommentcount/json/
返回登录用户所有博客的所有评论

5.
http://moonmonsters.pythonanywhere.com/api/ipsavernumbers/
获取每个IP地址的访问次数

6.
http://moonmonsters.pythonanywhere.com/api/ipsaverall/
获取所有的访问记录
