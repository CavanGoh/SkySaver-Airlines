package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@ComponentScan(basePackages = "com.example")
@EnableJpaRepositories(basePackages = "com.example.repo")
@EntityScan(basePackages = "com.example.model")
public class SeatServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(SeatServiceApplication.class, args);
    }
}
