package com.example

import com.auth0.jwt.JWT
import com.auth0.jwt.JWTVerifier
import com.auth0.jwt.algorithms.Algorithm
import java.util.*

object Auth {
    private const val SECRET_KEY = "secret"
    private val algorithm = Algorithm.HMAC512(SECRET_KEY)
    private const val issuer = "ktor.io"
    private const val validityInMs = 3600 * 1000 * 10 // 10 hours

    fun makeJwtVerifier(): JWTVerifier = JWT
        .require(algorithm)
        .withIssuer(issuer)
        .build()

    fun sign(name: String): Map<String, String> {
        return mapOf("token" to makeToken(name))
    }

    private fun makeToken(name: String): String = JWT.create()
        .withSubject("Authentication")
        .withIssuer(issuer)
        .withClaim("name", name)
        .withExpiresAt(getExpiration())
        .sign(algorithm)

    private fun getExpiration() = Date(System.currentTimeMillis() + validityInMs)

}