function getvector() {
    var formdata = new FormData();
    formdata.append('file', $('#file')[0].files[0]);
    var vector; //（2）且在ajax对全局变量进行设值
    $.ajax({
        url: 'http://122.112.159.211:233',
        type: 'post',
        processData: false,
        contentType: false,
        data: formdata,
        async: false, //（1）同步调用            
        success: function (data) {
            vector = "["+data.vector+"]";
            //document.getElementById("AjaxData")[0].value = vector;
            $("#AjaxData").val(vector);
            window.localStorage.setItem("FaceVector",data.vector);
            window.localStorage.setItem("FileName",data.fileName);
            //alert(vector);
            alert("图片上传成功");
        },
        error: function () {
            alert("上传失败！未识别到人脸！");
        }
    })
    //alert(vector);
    //return vector;               //(3)ajax函数外将变量return
}

function submitfaceId() {          
    var num = document.getElementById("Number").value;
    var na = document.getElementById("Name").value;
    var vec = document.getElementById("AjaxData").value;
    var userToken = window.localStorage.getItem("mytoken");
    //alert(userToken);
    if (num == "" || na == "" || "") { //要修改
        alert("填写的信息不能为空");
    }
    else if(vec == ""){
        alert("请先上传图片");
    }
    else {
        // alert(num);
        // alert(na);
        // alert(vec);
        $.ajax({
            //几个参数需要注意一下
            type: "POST", //方法类型
            url: "http://122.112.159.211/api/faceId", //url
            data:{
                number:num,
                name:na,
                vector:vec,
                fileName:window.localStorage.getItem("FileName")
            },
            headers: {
                'Authorization': 'Bearer ' + userToken
            },
            success: function (result) {

                alert(result);
                $("#Number").val("");
                $("#Name").val("");
                $("#AjaxData").val("");
                document.getElementById("file").value='';
            },
            error: function () {
                alert("录入失败!请重试或联系厂家！");
            }
        });

    }
}
function jump() {
    parent.document.location.href = "../html/records.html";
}
function jump_1() {
    parent.document.location.href = "../html/faceinfo.html";
}

function fileChange(target) {
        var fileSize = 0;
        fileSize = target.files[0].size;
        var size = fileSize / 1024;
        if(size>1000){
            alert("附件不能大于1M");
            target.value="";
            return false;   //阻止submit提交
        }
        var name=target.value;
        var fileName = name.substring(name.lastIndexOf(".")+1).toLowerCase();
        if(fileName !="jpg" && fileName !="png" && fileName !="jpeg" && fileName !="gif"){
            alert("请选择图片格式文件上传(jpg、png、jpeg、gif)！");
            target.value="";
            return false;   //阻止submit提交
        }
    }
