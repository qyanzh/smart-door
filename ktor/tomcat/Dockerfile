FROM tomcat
COPY ./wait-for-it.sh /usr/local/tomcat/bin/
RUN chmod +x /usr/local/tomcat/bin/wait-for-it.sh
CMD ["wait-for-it.sh", "cdb:3306", "--", "catalina.sh", "run"]