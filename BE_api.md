### 错误信息

​	当请求出错时，所有api返回如下错误信息。

* Response 200

````
{
  “success": 0,
  "err_msg": err_msg
}
````

### 用户组

用户使用账号密码登录。

更新了加密方式，采用django自带的登录模式

####通过用户名登录 `POST {base_url}/user/login`

*  Requset(application/json)

  `````Json
  {
    //email or username is all ok 
    "email": "qwer@qaz",
    "username": "zwexcelwang",
    "password":"madjadflas"  
  }
  `````

* Response 200

  ```Json
  {
    "success": 1,
    "username":"zwexcelwang"
  }
  ```

####注册用户 `POST{base_url}/user/sign`

* Request(application/json)

  ```Json
  {
    "email": "qwer@qaz", //FE do the Regex Filter
    "username":"zwexcelwang",  // username.length < 20 && FE check BE dosen't check
    "password":"askldfaffadk"  //  8 < length < 30
     "validate": "1234"
  }
  ```

* Response 200

  ````json
  {
  	"success":1,
  	"username": "zwexcelwang"
  }
  ````

####检查用户名或邮箱是否重复`GET{base_url}/user/sign`

* Requset(application/json)

````Json
{
  	//二选一
	"username": "zwexcelwang",
	"email": "qwer@qaz"
}
````

* Response 200

```Json
{
	"success": 1,
	"status": 0 // 1 for exists && 0 for not exist
}
```

####发送邮箱验证码`POST{base_url}/user/shortMess`

* Request (application/json)

```json
{
    "email": "qwer@qaz"
}
```

* Response 200

```Json
{
    "success": 1 //cant send again in 30 seconds
}
```

####用户登出`DELETE{base_url}/user/user`

* Request(application/json)

```Json
{
	"username": "zwexcelwang"
}
```

* Response 200

```Json
{
  "success":1
}
```

####修改密码`POST{base_url}/user/password`

* Request (application/json)

````Json
{
  "username":"zwexcelwang",
  "oldPassword":"mdadfjalfdj", // 8<length < 30
  "newPassword":"adjsflajadf", // 8<length < 30
}
````

* Response(application/json)

````Json
{
	"success" : 1
}
````

####忘记密码`PUT{base_url}/user/password`

//need to discuss

* Requset(application/json)

````json
{
	"username": "zwexcelwang",
  	"email": "qwer@qaz",
    "validate":"1234",
	"newPassword": "adfjadsag", // 8<length <30
}
````

* Response 200

```json
{
  "success": 1
}
```

### 答题模块

User chooses the course  =>  chooses years =>choose paper => gets problems  

####选择学科`GET{base_url}/course/course`  

// default Advanced  Mathmatics(need to discuss) 

* Request (application/json)

````Json
{
  "course": course_type  // 1 for advanced math 2 for linear algebra etc can discuss
}
````

* Response 200

```Json
{
    "success" : 1,
  	"num" : 10  //stands for the paper's number
  	"papers": [{
    	"paper_year" : 2016,
  		"paper_title" : "2016 Advanced Mathmatics A paper ",
  		"id" : 123124 // the only id BE use to select paper
	}, {
		"paper_year" : 2015,
      	"paper_title" : "2015 Advanced Mathmatics A paper",
      	"id" : 12312  // the only id BE use to select paper
    }]
}
```

####选择试卷`GET{base_url}/course/paper`

* Requeset(application/json)

```Json
{
    "paperId" : 123124
}
```

* Response 200

````Json
{
  "success" : 1,
  "ProblemNum": 20,
  "Problems": [{
    "ProblemId": 123213,
    "ProblemOrder": 1
  }, {
    "ProblemId": 12342,
    "ProblemOrder": 2
  }]  
  //ProblemId is the only id BE use to select problem
}
````

####选择题目`GET{base_url}/course/problem`

* Request(application/json)

```json
{
    "ProblemId": 12324,
  	"TimeSample": GMT Time // to record the time 
}
```

* Response 200

````json
{
  	"success": 1,
    "id": 1,
  	"pro_des": "I have no idea about the advanced mathmatics",
  //must support Latex
  	"pro_type": 1, // 1 for choose problem, 2 for judge problem, 3 for tiankong problem, 4 for Big problem
  	"pro_ans": "adfadsfadsf", // if type == 1 || type == 2 FE check the  answer
  	"pic" : url, // if url is null stands for no pic in this problem
}
````

####是否做对题目`POST{base_url}/course/`

//maybe change

* Requset(application/json)

```Json
{
  	"ProblemId": 12342,
  	"result": 1 // 0 for wrong && 1 for right
}
```

* Response 200

```json
{
  "success": 1
}
```

####加入错题本`POST{base_url}/course/record`

//Maybe change

* Request(application/json)

````Json
{
	"ProblemId": 123442,
	"username": "zwexcelwang" // but actually zwexcelwang stands for ALWAYS RIGHT ANSWRONG
}
````

* Response 200

```Json
{
    "success": 1
}
```

####题目报错`POST{base_url}/course/`

//maybe change

* Requese(application/json)

```Json
{
  	"ProblemId": 2132421,
  	"username": "zwexcelwang"，
	"reason":"describe the wrong points something like the print wrong or answer wrong"
}
```
* Response 200

```Json
{
  "success": 1
}
```

####查看错题统计`GET{base_url}/course/record`

//maybe FE can do that 

* Request  (application/json)

```Json
{
	"username": "zwexcelwang",
}
```

* Response 200

```Json
{
    "problemNum": 123
  	"problems":[
    	{
    	"problemId": 1231234,
  		"problemDes": " " //descrbe the problem
	},{
       	"problemId": 123423,
      	"problemDes": " "
    }
  ]
}
```

If user want do that again, go to the 选择题目 funtion。