package com.example

import io.ktor.application.Application
import org.slf4j.LoggerFactory

val logger = LoggerFactory.getLogger(Application::class.java)

fun debug(msg: String?) {
    msg?.let {
        logger.debug(msg)
    }
}