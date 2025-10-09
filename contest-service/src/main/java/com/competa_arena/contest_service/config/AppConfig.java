package com.competa_arena.contest_service.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {

    @Value("${user.service.url}")
    private String userServiceUrl;

    public String getUserServiceUrl() {
        return userServiceUrl;
    }
}
