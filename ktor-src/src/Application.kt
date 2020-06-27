package com.example

import com.fasterxml.jackson.databind.SerializationFeature
import io.ktor.application.Application
import io.ktor.application.ApplicationCallPipeline
import io.ktor.application.call
import io.ktor.application.install
import io.ktor.auth.Authentication
import io.ktor.auth.UserIdPrincipal
import io.ktor.auth.authenticate
import io.ktor.auth.authentication
import io.ktor.auth.jwt.jwt
import io.ktor.client.HttpClient
import io.ktor.client.request.forms.submitForm
import io.ktor.features.ContentNegotiation
import io.ktor.features.DefaultHeaders
import io.ktor.features.origin
import io.ktor.http.HttpHeaders
import io.ktor.http.HttpMethod
import io.ktor.http.HttpStatusCode
import io.ktor.http.content.PartData
import io.ktor.http.content.readAllParts
import io.ktor.http.content.streamProvider
import io.ktor.http.parametersOf
import io.ktor.jackson.jackson
import io.ktor.request.httpMethod
import io.ktor.request.receiveMultipart
import io.ktor.request.receiveParameters
import io.ktor.response.respond
import io.ktor.response.respondFile
import io.ktor.routing.get
import io.ktor.routing.post
import io.ktor.routing.route
import io.ktor.routing.routing
import java.io.File

//fun main(args: Array<String>): Unit = io.ktor.server.netty.EngineMain.main(args)

@Suppress("unused") // Referenced in application.conf
fun Application.module() {

    initDB()

    intercept(ApplicationCallPipeline.Call) {
        if (call.request.httpMethod == HttpMethod.Options)
            call.respond(HttpStatusCode.OK)
    }

    install(DefaultHeaders) {
        // cross-domain
        header(HttpHeaders.AccessControlAllowOrigin, "*")
        header(HttpHeaders.AccessControlAllowHeaders, "*")
    }

    install(Authentication) {
        jwt {
            verifier(Auth.makeJwtVerifier())
            validate {
                UserIdPrincipal(it.payload.getClaim("name").asString())
            }
        }
    }

    install(ContentNegotiation) {
        jackson {
            enable(SerializationFeature.INDENT_OUTPUT)
        }
    }

    routing {

        post("/login") {
            val param = call.receiveParameters()
            val username = param["username"]!!
            val password = param["password"]!!
            if (DB.login(username, password)) {
                call.token(username)
            } else {
                call.error("账号或密码错误")
            }
        }

        authenticate {

            /* 签到 */
            post("/sign") {
                val multipart = call.receiveMultipart().readAllParts()
                val number = (multipart.filter { it.name == "number" }[0] as PartData.FormItem).value
                val filePart = (multipart.filter { it.name == "photo" }[0] as PartData.FileItem)
                val temperature = (multipart.filter { it.name == "temperature" }[0] as PartData.FormItem).value
                val ext = File(filePart.originalFileName ?: "0.jpg").extension
                val filename = "sign-${number}-${System.currentTimeMillis()}.$ext"
                val file = File("/photos", filename)
                filePart.streamProvider().use { input ->
                    file.outputStream().buffered().use { output -> input.copyToSuspend(output) }
                }
                call.authentication.principal<UserIdPrincipal>()?.apply {
                    if (DB.sign(name, number, filename, temperature)) {
                        call.success("${number}使用${name}签到成功")
                    } else {
                        call.error("录入数据库失败")
                    }
                    if (temperature.toFloat() > 37.2) {
                        HttpClient().submitForm<Any>(
                            "http://122.112.159.211:234",
                            parametersOf("Body", "学号：$number 体温：$temperature 签到设备：$name")
                        )
                    }
                } ?: run {
                    val ip = call.request.origin.remoteHost
                    if (DB.sign(ip, number, filename, temperature)) {
                        call.success("${number}使用${ip}签到成功")
                    } else {
                        call.error("录入数据库失败")
                    }
                }
            }

            get("/sync") {
                val param = call.parameters
                val time = param["lastTime"]?.toLong() ?: 0L
                val list = DB.getFaces(time)
                call.respond(list)
            }

            route("/faceId") {
                /* 录入 */
                post("/") {
                    val param = call.receiveParameters()
                    val number = param["number"]!!
                    val name = param["name"]!!
                    val vector = param["vector"]!!
                    val fileName = param["fileName"] ?: ""
                    if (DB.faceId(number, name, vector, fileName)) {
                        call.success("$number $name 录入成功")
                    } else {
                        call.error("录入失败")
                    }
                }

                post("/delete") {
                    val param = call.receiveParameters()
                    val number = param["number"]
                    number?.let {
                        if (DB.deleteFace(it)) {
                            call.success("删除人脸成功")
                        } else {
                            call.error("删除失败")
                        }
                    } ?: run {
                        call.error("缺少参数number")
                    }
                }

            }

            get("/records") {
                val param = call.parameters
                val time = param["lastTime"]?.toLong() ?: 0L
                val list = DB.getRecords(time)
                call.respond(HttpStatusCode.OK, list)
            }

            get("/faces") {
                val param = call.parameters
                val time = param["lastTime"]?.toLong() ?: 0L
                val list = DB.getFacesWithImg(time)
                call.respond(list)
            }

        } // authenticate

        /* 图片 */
        get("/img") {
            val photo = call.parameters["photo"]!!
            val file = File("/photos", photo)
            if (file.exists()) {
                call.respondFile(file)
            } else {
                call.error("文件不存在")
            }
        }
    }
}
