#MiXin API接口研究

本说明参考@李林的[开发者接入Mixin Network说明](https://gist.github.com/myrual/64769acd3d09e9fd3ac37636d899f844#%E5%BC%80%E5%8F%91%E8%80%85%E6%8E%A5%E5%85%A5mixin-network%E8%AF%B4%E6%98%8E)

##1 获取某个MiXin app用户的信息

`https://mixin.one/oauth/authorize?client_id=Client_ID&scope=PROFILE:READ`

Client_ID为dashbord里面那个UUID的字符串，也就是那个 7921bb6f-f2e0-4ecd-a58e-e126c0437ed2 样子的字符串。

SCOPE可以是如下组合：

```
PROFILE:READ
PROFILE:READ+PHONE:READ
PROFILE:READ+ASSETS:READ
PROFILE:READ+PHONE:READ+ASSETS:READ
```

扫描之后返回

`[The OAuth redirect uri]/?code=8ed31bbe5619174691a5a010d513a1983236a9ed85942a01eac0eb566466be36`

这样的一串结果。


