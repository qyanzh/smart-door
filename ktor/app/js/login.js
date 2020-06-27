
function loginup() {
    
    var un = document.getElementById("userNname").value;
    var pw = document.getElementById("password").value;
    if (un == "" || pw == "") {
        alert("用户名或密码不能为空！");
    } else {
        $.ajax({
            //几个参数需要注意一下
            type: "POST", //方法类型
            url: "http://122.112.159.211:80/api/login", //url
            data: $('#lfsubmit').serialize(),
            success: function (data) {
                //alert("...");
                const token = data.token;                
                window.localStorage.setItem('mytoken',token);
                parent.document.location.href = "../html/frame.html";
            },
            error: function () {
                alert("账户不存在或者密码错误！请重新输入！");
            }
        });

    }
}