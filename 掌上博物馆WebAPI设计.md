### 掌上博物馆WebAPI设计

主机：host  端口：port

根目录(root)：http://host:port/api/

一些说明：

- 无论数据的上传或是返回均采用json格式

- 未作具体说明的**状态码**统一约定：
  
  - 200, 提交成功或删除成功, 返回`success`
  - 403, 用户未登录或权限不够, 返回`Login Required` 
  - 404, 请求的数据不存在, 返回`Not Found`

- GET方法中若注明了limit和page参数则每次请求时请务必加上这两个参数

- 图片音视频url约定：返回的url不是全部的url需要在本地进行拼接, 方式为加上http://host:port/的前缀

#### 注册视图

+ url : root/register/

+ POST方法 数据：
  
  示例：
  
  ```json
  {
      "username" : "john",
      "email" : "john3768@gmail.com",
      "password" : "wjdbbsmcns",
  }
  ```

+ 返回状态码及数据
  
  + 200, 注册成功
  
  + 403, 用户名或邮箱不唯一, 返回数据：`email registered`（邮箱不唯一）, `username registered`（用户名不唯一）

#### 登录视图

+ url : root/login/

+ POST方法数据: 
  
  上传**用户名与密码**或者**邮箱与密码**
  
  示例：
  
  ```json
  {
      "username" : "john", 
      "password" : "wjdbbsmcns"
  }
  ```
  
  or
  
  ```json
  {
      "email" : "john3768@gmail.com", 
      "password" : "wjdbbsmcns"
  }
  ```

+ 返回状态码及数据：
  
  + 200, 登录成功, 返回 用户信息, 示例
    
    ```json
    {
        "username" : "john", 
        "email" : "john3768@gmail.com", 
        "gender" : "m",
        "loaction" : "北京 朝阳",
        "desc" : "good!",
        "pic_url" : "/media/user_pics/john_pic.png"
    }
    ```
  
  + 403, 登录失败, 返回信息, 
    
    - `username not found` 用户名未找到
    - `email not found` 邮箱未找到
    - `wrong password` 密码错误

+ **注意** ：登录成功后返回的cookies应该保存为全局变量, 以后每次发送请求时务必将cookies设置为该cookies

#### 登出视图

+ url : root/logout/
+ 方法 GET
+ 数据：无
+ 返回状态码：200，登出成功
+ **注意**：之所以不需要POST数据是因为用户的信息保存在cookies中，所以发送请求时务必设置cookies为登录后返回的cookies

#### 文物视图

##### 请求多个文物

+ url : root/objects/,  不需要验证用户是否登录

+ GET方法（文物的关键字搜索，分类搜索等等）：
  
  + 数据
    
    + 每页个数==**limit**===...
    
    + 页码==**page**===...
    
    + 博物馆 museum=... 
      
      可用选项
      
      ```
      - Freersackler
      - Rubin Museum
      - Denver Art MUseum
      - David Owsley Museum of Art
      - Asia Society Museum
      ```
    
    + 来源地 location=...
      
      可用选项
      
      ```
      {
          "江苏" : "Jiangsu",
          "江西" : "Jiangxi",
          "安徽" : "Anhui",
          "湖北" : "Hebei",
          "山西" : "Shanxi",
          "浙江" : "Zhejiang",
          "陕西" : "Shaanxi",
          "河南" : "Henan",
          "福建" : "Fujian",
          "广东" : "Guangdong",
          "甘肃" : "Gansu",
          "云南" : "Yunnan",
          "山东" : "Shandong",
          "湖南" : "Hunan",
          "湖北" : "Hubei",
          "四川" : "Sichuan",
          "新疆" : "Xinjiang",
          "广西" : "Guangxi",
          "西藏" : "Tibet",
          "中国" : "China",
          "美国" : "United States",
          "英国" : "England",
          "日本" : "Japan",
          "朝鲜" : "Korea",
      }
      ```
    
    + 年代 dynasty=...
      
      可用选项
      
      ```
      Neolithic period //新石器时代
      
      Shang dynasty //商朝
      Anyang period //商朝
      Middle Shang dynasty //商朝中期
      
      Zhou dynasty //周朝
      Western Zhou dynasty //西周
      Eastern Zhou dynasty //东周
      Warring States period //战国
      
      Han dynasty //汉朝
      Eastern Han dynasty //东汉
      Western Han dynasty //西汉
      
      Western Jin dynasty //东晋
      
      Northern Qi //北齐
      Northern Song dynasty //北宋
      Northern Wei dynasty //北魏
      Western Wei dynasty //西魏
      Southern Dynasties //南朝
      Northern Dynasties //北朝
      
      Sui dynasty //隋朝
      
      Tang dynasty //唐朝
      
      Song dynasty //宋朝
      Northern Song //北宋
      Southern Song dynasty //南宋
      
      Yuan dynasty //元朝
      
      Ming dynasty //明朝
      
      Qing dynasty //清朝
      
      Modern period //现代
      ```
    
    + 材质 medium=...
      
      可用选项
      
      ```
      lacquer, Lacquered, wood//木漆器
      Bronze //青铜
      Brocade, Silk // 丝绸
      Ceramic, Porcelain // 陶瓷
      Clay //粘土
      Crystal //水晶
      Earthenware, Stone, Stoneware, terracotta//石器
      Gold, Gilt //镀金
      Silver // 银器
      hanging scroll, ink, colors, paper//水墨画
      Oil // 油画
      horn // 角制品
      Iron // 铁器
      Ivory //象牙
      Jade //玉器
      feather //羽毛
      Limestone //石灰石
      Marble //大理石
      Bone//骨制品
      glass //玻璃制品
      ```
    
    + 搜索 search=...
  
  + 返回状态码及数据：
    
    + 200, 查找成功, 返回数据：搜索到的文物信息列表, 示例：
      
      ```json
      {
          "data" : [
                      {
                          "id" : 13623,
                          "name" : "Minqing ware bowl",
                          "img_url" : "FS-7903_05,FS-7903_06", //图片链接
                          "museum" : "Freersackler", //所属博物馆
                          "time_period" : "Southern Song dynasty",//所属时期
                          "location" : null,//来源地
                          "like_times" : 3456, //点赞次数
                          "comment_times" : 356, //评论次数
                      },
                      {
                          //...
                      }
                  ],
          "count" : 1234,
          "page_num" : 10,
      }
      ```
    
    + 404

+ POST方法（**以图搜图**）：
  
  + 数据
    + image，即要搜索的图片
  + 返回状态码及数据
    + 200, 查找成功, 返回数据：匹配到的文物信息列表（jsonarray）, 示例同上
    + 404

##### 请求单个文物

+ url : root/object/id/ , 不需要验证用户是否登录, id 为文物id

+ GET方法
  
  + 数据：无
  
  + 返回状态码及数据：
    
    + 200, 查找成功, 返回数据：找到的单个文物信息, 示例：
      
      ```json
      {
          "id": 102,
          "name": "Cottage in the Mountains",
          "img_url": "49baf7da34d9f7a8d4652a86a8cd7eb2",
          "museum": "Freersackler",
          "location": "Yunnan",
          "time_period": "1644~1911",
          "dynasty": "清朝",
          "like_times": 2,
          "comment_times": 13,
          "bibliography": "Richard Edwards. The Painting of Tao-chi, 1641-ca.1720. Exh. cat. Ann Arbor. p. 101.Wen C. Fong. Images of the Mind: Selections from the Edward L. Elliott Family and John B. Elliott Collections of Chinese Calligraphy and Painting at the Art Museum, Princeton University. Exh. cat. Pinceton. p. 207.Kathleen Yang. Through a Chinese Connoisseur's Eye: Private Notes of C.C. Wang. Beijing. p.343, fig.133.",
          "credit": "Purchase — Charles Lang Freer Endowment and the Collections Acquisitions Program",
          "dimensions": "H x W (image): 108.6 x 52 cm (42 3/4 x 20 1/2 in)",
          "label": null,
          "medium": "Hanging scroll; ink and color on paper",
          "object_type": "Freer Gallery of Art",
          "previous_owner": "C.C. Wang China,1907-2003; active United States",
          "provenance": null,
          "url": "https://asia.si.edu/object/F1982.23",
          "cat1": null,
          "cat2": "Qing dynasty",
          "cat3": "Painting,",
          "makers_born": "1642-1707,",
          "makers_name": "Shitao,",
          "makers_job": "Artist,",
          "object_id": "F1982.23"
      }
      ```
    
    + 404

#### 用户信息视图

**需要用户登录**

+ url : root/user/username/, username为用户名

+ GET方法
  
  + 数据：无
  
  + 返回状态码及数据：
    
    + 200, 查找成功, 返回数据：用户个人信息, 示例：
      
      ```json
      {
          "username" : "john", 
          "email" : "john3768@gmail.com", 
          "gender" : "m",
          "loaction" : "北京 朝阳",
          "desc" : "good!",
          "pic_url" : "/media/user_pics/john_pic.png",
      }
      ```
    
    + 404
    
    + 403

+ PUT方法(修改个人信息)
  
  + 数据：
    
    ```json
    // 头像图片上传
    // or 修改个人描述
    {
        "desc" : "Good!"
    }
    ```
  
  + 返回数据及状态码
    
    + 200, 修改成功, 返回修改后的个人数据
    
    + 403
    
    + 404

#### 用户动态视图

##### 多个用户动态

+ url : root/dynamics/

+ GET方法：
  
  + 数据：
    
    + 每页个数==limit===...
    
    + 页码==page===...
    
    + objectid=...(获取针对某个文物的动态)
    
    + username=...(获取某个人所有的动态)
  
  + 返回数据及状态码
    
    - 200, 查找成功, 返回数据如下
      
      ```json
      {
          "data": [
              {
                  "id": 16,
                  "objectid": null,
                  "user": "huhu",
                  "text": "vedio test",
                  "files_urls": "16trailer.mp4,",
                  "time": "2022-05-16 17:10:50.594680",
                  "like_times": 0,
                  "comment_times": 0
              },
              {
                  "id": 13,
                  "objectid": null,
                  "user": "huhu",
                  "text": "picture test8",
                  "files_urls": "13下载 (3).jpeg,13下载.jpeg,",
                  "time": "2022-05-16 16:47:07.751954",
                  "like_times": 0,
                  "comment_times": 0
              }
          ],
          "count": 14,
          "page_num": 5
      }
      ```
    
    - 403
    
    - 404

+ POST方法
  
  + 数据示例：
    
    使用**form-data**
    
    + **data**:
      
      ```
      {
          "user" : "john",
          "objectid" : null,
          "text" : "hello!"
      }
      ```
    - **images**: 具体的图片
    
    - **audios**:  具体的音频
    
    - **vedios**:  具体的视频

+ 返回数据及状态码
  
  - 200
    
    ```json
    {
        "id": 11,
        "objectid": null,
        "user": "huhu",
        "text": "picture test7",
        "files_urls": "11下载 (3).jpeg,11下载.jpeg,",
        "time": "2022-05-16 16:28:06.072535",
        "like_times": 0,
        "comment_times": 0
    }
    ```
  
  - 403

##### 单个用户动态

+ url : root/dynamic/id/, id为用户动态id

+ GET方法
  
  - 数据：null
  
  - 返回状态码及数据
    
    - 200, 获取成功, 返回数据：
      
      ```json
      {
          "id" : 2,
          "user" : "john",
          "objectid" : null,
          "text" : "hello world!",
          "files_urls" : null,
          "time" : "2022-4-25-02-30-30"
      }
      ```
    
    - 403
    
    - 404

+ DELETE方法
  
  + 数据：null
  
  + 返回状态码及数据
    
    - 200
    
    - 403
    
    - 404

#### 用户评论视图

##### 多个用户评论

+ url : root/comments/

+ GET方法
  
  + 数据：
    
    - limit=...
    
    - page=...
    + objectid=...(显示文物评论)
    
    + dynamicid=...(显示动态评论)
    
    + commentid=...(显示对某个评论的回复)
    
    + user=...(显示某用户所有评论)
  
  + 返回状态码及数据：
    
    + 200, 获取成功,  数据示例：
      
      ```json
      {
          "data": [
              {
                  "id": 13,
                  "user": "john",
                  "objectid": 102,
                  "dynamicid": null,
                  "commentid": null,
                  "reply_user": null,
                  "time": "2022-05-18 12:10",
                  "text": "评论测试",
                  "images": null,
                  "like_times": 0
              },
              {
                  "id": 15,
                  "user": "123456",
                  "objectid": 102,
                  "dynamicid": null,
                  "commentid": null,
                  "reply_user": null,
                  "time": "2022-05-18 18:48",
                  "text": "不错。",
                  "images": null,
                  "like_times": 0
              }
          ],
          "count": 13,
          "page_num": 7
      }
      ```
    
    + 403
    
    + 404

+ POST方法
  
  + 数据示例：
    
    使用**form-data**:
    
    **data**:
    
    ```json
    {
        "user" : "john",
        "objectid" : 1,
        "dynamicid" : null,
        "commentid" : 2,
        "text" : "john reply"
    }
    ```
    
    **image**:相应图片

+ 返回状态码及数据：
  
  - 200
  - 403

##### 单个用户评论

+ url : root/comment/id/

+ GET方法
  
  - 数据：null
  
  - 返回状态码及数据：
    
    - 200, 查询成功, 返回数据示例
      
      ```json
      {
          "id" : 5,
          "user" : "john", //评论发布用户
          "objectid" : 1,
          "dynamicid" : null, 
          "commentid" : 1,
          "reply_user" : "Mike", //回复给的用户
          "text" : "hello world!",
          "images" : "media/commment_pics/5_test.png",
          "time" : "2022-3-29-00-00-00",
          "like_times" : 2,
      }
      ```
    
    - 403
    
    - 404

+ DELETE方法
  
  + 数据：null
  + 返回状态码及数据：
    - 200
    - 403
    - 404

#### 用户点赞视图

##### 点赞列表获取及点赞提交

+ url : root/stars/

+ GET方法：
  
  - 数据：
    
    - limit=...
    - page=...
    - username=...&type=...(用户赞过的文物, 动态, 评论查询, type取值, 'object', 'dynamic', 'comment')
    - objectid=...(赞过某一文物的用户查询)
    - dynamicid=...(赞过某一动态的用户查询)
    - commentid=...(赞过某一评论的用户查询)
  
  - 返回状态码及数据
    
    - 200, 请求成功, 返回数据示例：
      
      ```json
      {
          "data": [
              {
                  "id": 84,
                  "user": "john",
                  "objectid": 102,
                  "dynamicid": null,
                  "commentid": null,
                  "time": "2022-05-20 10:21:07.172494"
              },
              {
                  "id": 61,
                  "user": "123456",
                  "objectid": 102,
                  "dynamicid": null,
                  "commentid": null,
                  "time": "2022-05-18 22:27:38.471453"
              }
          ],
          "count": 2,
          "page_num": 1
      }
      ```
    
    - 403
    
    - 404

+ POST方法
  
  - 数据示例：
    
    ```json
    //文物点赞
    {
        "user" : "john",
        "objectid" : 1,
    }
    ```
    
    ```json
    // or 动态点赞
    {
        "user" : "john",
        "dynamicid" : 3,
    }
    ```
    
    ```json
    //or 评论点赞
    {
        "user" : "john",
        "commentid" : 5,
    }
    ```
  
  - 返回状态码及数据
    
    - 200
    - 403

##### 单个点赞

+ url : root/star/id/

+ GET方法：
  
  - 数据：null
  
  - 返回状态码及数据
    
    - 200, 获取成功, 返回数据示例
      
      ```json
      {
          "id" : 3,
          "user" : "john",
          "objectid" : 1,
          "dynamicid" : null,
          "commentid" : null,
          "time" : "2022-4-29-00-00-00",
      }
      ```
    
    - 403
    
    - 404

+ DELETE方法：
  
  + 数据：null
  + 返回状态码及数据：
    - 200
    - 403
    - 404

#### 用户关注视图

##### 关注列表获取及关注提交

+ url : root/attentions/

+ GET方法：
  
  - 数据：
    
    - limit=...
    
    - page=...
    
    - type=...(type取值, `followed` 我关注的, `follow` 关注我的)
      
      示例：`root/attentions/?type=follow`
  
  - 返回状态码及数据
    
    - 200, 查询成功, 返回数据示例如下：
      
      我(john)关注的
      
      ```json
      [
          {
              "id" : 1,
              "from_user" : "john",
              "to_user" : "Mike",
              "time" : "2022-4-29-00-00-00"
          },
          {
              "id" : 2,
              "from_user" : "john",
              "to_user" : "Jordan",
              "time" : "2022-4-28-13-01-45"
          }
      ]
      ```
      
      关注我(john)的
      
      ```json
      [
          {
              "id" : 3,
              "from_user" : "Mike",
              "to_user" : "john",
              "time" : "2022-4-28-11-02-15"
          },
          {
              "id" : 4,
              "from_user" : "Jordan",
              "to_user" : "john",
              "time" : "2022-4-24-06-02-15"
          }
      ]
      ```
    
    - 403
    
    - 404

+ POST方法
  
  + 数据示例：
    
    ```json
    {
        "from_user" : "john",
        "to_user" : "Mike"
    }
    ```
  
  + 返回状态码及数据：
    
    - 200
    - 403

##### 取消关注

+ url : root/attention/id/

+ DELETE方法：
  
  + 数据：null
  + 返回状态码及数据：
    - 200
    - 403
    - 404

#### 用户通知视图

说明：用户通知数据 在 客户端提交其他数据的时候会自动生成, 无需post方法对用户通知信息进行提交

##### 用户通知获取

+ url : root/notifications/

+ GET方法：
  
  - 数据：
    
    - limit=...
    - page=...
  
  - type=...(type取值, `unread`未读, `read`已读)
  
  - 返回状态码及数据：
    
    - 200, 获取成功, 返回数据示例
      
      ```json
      /*
      type:
      ('f', 'follow'),  # 关注了你 commentid和starid均为None
      
      ('c', 'comment'), # 评论了你 comentid有值,
                        # 通过commentid查询具体的comment可知具体内容
                        # 具体内容(评论了具体哪条动态)
      
      ('l', 'like'),    # 赞了你 starid有值
      
      ('r', 'reply'),   # 回复了你 commentid有值
                        # 通过commentid查询具体的comment可知具体内容
                        # 具体内容(回复了哪条评论，属于哪个文物或哪个动态)
      */
      /*
      read:
      '0' : 未读
      '1' : 已读
      */
      [
          //Mike评论了你的动态
          {
              "id" : 1,
              "user" : "john",
              "action_user" : "Mike",
              "type" : "comment",
              "starid" : null,
              "commentid" : null,
              "read" : "0",
          },
          //Jordan关注了你
          {
              "id" : 2,
              "user" : "john",
              "action_user" : "Jordan",
              "type" : "follow",
              "starid" : null,
              "commentid" : null,
              "read" : '1',
        }
          //其他类型同上👆
      ]
      ```
    
    - 403
    
    - 404

##### 已读提交

+ url : root/notification/id/

+ PUT方法：
  
  + 数据示例：
    
    ```json
    //只需要一个read数据就行
    {
        "read" : '1',
    }
    ```
  
  + 返回状态码及数据：
    
    - 200
    - 403
    - 404 
