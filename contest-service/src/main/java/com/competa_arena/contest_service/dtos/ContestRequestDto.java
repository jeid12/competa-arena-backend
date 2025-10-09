package com.competa_arena.contest_service.dtos;

import java.time.LocalDateTime;
import java.util.List;

public class ContestRequestDto {

    private String title;
    private String subject; // Math, Physics, ComputerScience
    private String visibility; // public/private

    private List<QuestionDto> questions;

    private LocalDateTime startTime;
    private LocalDateTime endTime;

    // Getters & Setters
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getSubject() { return subject; }
    public void setSubject(String subject) { this.subject = subject; }

    public String getVisibility() { return visibility; }
    public void setVisibility(String visibility) { this.visibility = visibility; }

    public List<QuestionDto> getQuestions() { return questions; }
    public void setQuestions(List<QuestionDto> questions) { this.questions = questions; }

    public LocalDateTime getStartTime() { return startTime; }
    public void setStartTime(LocalDateTime startTime) { this.startTime = startTime; }

    public LocalDateTime getEndTime() { return endTime; }
    public void setEndTime(LocalDateTime endTime) { this.endTime = endTime; }
}
