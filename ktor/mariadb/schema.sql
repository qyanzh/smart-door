create database ktor;

create user 'ktor_user' @'%' identified by '1234';

grant all on ktor.* to 'ktor_user' @'%';