package com.competa_arena.contest_service.config;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.filter.OncePerRequestFilter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;

@Component
public class JwtAuthorizationFilter extends OncePerRequestFilter {

    private static final Logger logger = LoggerFactory.getLogger(JwtAuthorizationFilter.class);

    @Autowired
    private AppConfig appConfig;

    private final RestTemplate restTemplate = new RestTemplate();

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
            throws ServletException, IOException {

        String path = request.getRequestURI();
        String method = request.getMethod();

        logger.info("Incoming request: {} {}", method, path);

        String authHeader = request.getHeader("Authorization");
        logger.debug("Authorization Header: {}", authHeader);

        if (!StringUtils.hasText(authHeader) || !authHeader.startsWith("Bearer ")) {
            if ("GET".equalsIgnoreCase(method)) {
                logger.info("No Authorization header but GET request allowed for {}", path);
                filterChain.doFilter(request, response);
                return;
            } else {
                logger.warn("Unauthorized request: Missing or invalid token");
                response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Missing or invalid Authorization header");
                return;
            }
        }

        String token = authHeader.replace("Bearer ", "");
        String userServiceUrl = appConfig.getUserServiceUrl() + "/api/token/validate-token";

        try {
            logger.info("Validating token with user service: {}", userServiceUrl);

            HttpHeaders headers = new HttpHeaders();
            headers.setBearerAuth(token);
            HttpEntity<Void> entity = new HttpEntity<>(headers);

            ResponseEntity<UserValidationResponse> res = restTemplate.exchange(
                    userServiceUrl,
                    HttpMethod.GET,
                    entity,
                    UserValidationResponse.class
            );

            logger.debug("Response from user service: {}", res);

            if (!res.getStatusCode().is2xxSuccessful() || res.getBody() == null) {
                logger.error("Invalid token - user service returned: {}", res.getStatusCode());
                response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Invalid token");
                return;
            }

            String role = res.getBody().getRole();
            logger.info("User validated. Role: {}, UserID: {}", role, res.getBody().getUserId());

            if ((method.equals("POST") || method.equals("PUT") || method.equals("DELETE")) &&
                    !role.equalsIgnoreCase("CREATOR") && !role.equalsIgnoreCase("ADMIN")) {
                logger.warn("Access denied for role {} on method {}", role, method);
                response.sendError(HttpServletResponse.SC_FORBIDDEN, "Insufficient role");
                return;
            }

            request.setAttribute("userId", res.getBody().getUserId());
            request.setAttribute("role", role);

        } catch (Exception e) {
            logger.error("JWT validation error: {}", e.getMessage(), e);
            response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Unauthorized: " + e.getMessage());
            return;
        }

        filterChain.doFilter(request, response);
    }

    public static class UserValidationResponse {
        private String userId;
        private String role;

        public String getUserId() { return userId; }
        public void setUserId(String userId) { this.userId = userId; }

        public String getRole() { return role; }
        public void setRole(String role) { this.role = role; }
    }
}
