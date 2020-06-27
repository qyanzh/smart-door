package com.example

import org.jetbrains.exposed.dao.IntEntity
import org.jetbrains.exposed.dao.IntEntityClass
import org.jetbrains.exposed.dao.id.EntityID
import org.jetbrains.exposed.dao.id.IntIdTable
import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.SchemaUtils
import org.jetbrains.exposed.sql.SortOrder
import org.jetbrains.exposed.sql.deleteWhere
import org.jetbrains.exposed.sql.transactions.transaction

fun initDB() {
    val host = "cdb:3306"
//    val host = "localhost:3336"
    Database.connect(
        "jdbc:mysql://${host}/ktor?useSSL=no&allowPublicKeyRetrieval=true", driver = "com.mysql.jdbc.Driver",
        user = "root", password = "1234"
    )
    transaction {
        SchemaUtils.createMissingTablesAndColumns(Faces, Managers, Records)
    }
}

object Managers : IntIdTable() {
    val username = varchar("username", length = 20).uniqueIndex()
    val password = varchar("password", length = 20)
}

class Manager(id: EntityID<Int>) : IntEntity(id) {
    companion object : IntEntityClass<Manager>(Managers)

    var username by Managers.username
    var password by Managers.password
}

object Faces : IntIdTable() {
    val number = varchar("number", length = 9).uniqueIndex()
    val name = varchar("name", length = 50)
    val vector = varchar("vector", length = 5000)
    val time = long("time")
    val fileName = varchar("fileName", length = 50)
}

class Face(id: EntityID<Int>) : IntEntity(id) {
    companion object : IntEntityClass<Face>(Faces)

    var number by Faces.number
    var name by Faces.name
    var vector by Faces.vector
    var time by Faces.time
    var fileName by Faces.fileName
}

data class FaceDTO(val number: String, val name: String, val vector: String)

data class FaceImgDTO(val number: String, val name: String, val fileName: String)

object Records : IntIdTable() {
    val manager = varchar("manager", length = 30)
    val number = varchar("number", length = 9)
    val time = long("time")
    val fileName = varchar("fileName", length = 50)
    val temperature = varchar("temperature", length = 10)
}

class Record(id: EntityID<Int>) : IntEntity(id) {
    companion object : IntEntityClass<Record>(Records)

    var manager by Records.manager
    var number by Records.number
    var time by Records.time
    var fileName by Records.fileName
    var temperature by Records.temperature
}

data class RecordDTO(
    val manager: String,
    val number: String,
    val name: String,
    val time: Long,
    val fileName: String,
    val temperature: String
)

object DB {

    fun login(username: String, password: String) = transaction {
        Manager.find { Managers.username eq username }.firstOrNull()?.let {
            it.password == password
        } ?: run {
            false
        }
    }


    fun faceId(number: String, name: String, vector: String, fileName: String) = transaction {
        Face.find { Faces.number eq number }.firstOrNull()?.let {
            it.number = number
            it.name = name
            it.vector = vector
            it.time = System.currentTimeMillis()
            it.fileName = fileName
        } ?: run {
            Face.new {
                this.number = number
                this.name = name
                this.vector = vector
                this.time = System.currentTimeMillis()
                this.fileName = fileName
            }
        }
        true
    }

    fun getFaces(lastTime: Long) = transaction {
        Face.find { Faces.time greater lastTime }.map {
            FaceDTO(it.number, it.name, it.vector)
        }
    }

    fun getFacesWithImg(lastTime: Long) = transaction {
        Face.find { Faces.time greater lastTime }.map {
            FaceImgDTO(it.number, it.name, it.fileName)
        }
    }

    fun deleteFace(number: String) = transaction {
        1 == Faces.deleteWhere { Faces.number eq number }
    }

    fun getRecords(startTime: Long) = transaction {
        Record.find { (Records.time greater startTime) }.orderBy(Records.time to SortOrder.DESC).map {
            val name = Face.find { Faces.number eq it.number }.firstOrNull()?.name ?: "未知"
            RecordDTO(it.manager, it.number, name, it.time, it.fileName, it.temperature)
        }
    }

    fun sign(manager: String, number: String, fileName: String, temperature: String) = transaction {
        Record.new {
            this.manager = manager
            this.number = number
            this.time = System.currentTimeMillis()
            this.fileName = fileName
            this.temperature = temperature
        }
        true
    }

}



