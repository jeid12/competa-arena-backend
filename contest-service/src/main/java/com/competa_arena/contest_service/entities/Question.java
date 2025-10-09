package com.competa_arena.contest_service.entities;

import java.util.List;

public class Question {

    private String type; // MCQ, SHORT_ANSWER, PROGRAMMING
    private String question;

    // MCQ only
    private List<String> options;
    private String answer;

    // Short Answer
    private String expectedAnswer;

    // Programming
    private String statementFile; // URL to PDF
    private String testCaseFile;  // URL to TXT
    private List<String> language; // Allowed languages for programming

    // Getters & Setters
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }

    public String getQuestion() { return question; }
    public void setQuestion(String question) { this.question = question; }

    public List<String> getOptions() { return options; }
    public void setOptions(List<String> options) { this.options = options; }

    public String getAnswer() { return answer; }
    public void setAnswer(String answer) { this.answer = answer; }

    public String getExpectedAnswer() { return expectedAnswer; }
    public void setExpectedAnswer(String expectedAnswer) { this.expectedAnswer = expectedAnswer; }

    public String getStatementFile() { return statementFile; }
    public void setStatementFile(String statementFile) { this.statementFile = statementFile; }

    public String getTestCaseFile() { return testCaseFile; }
    public void setTestCaseFile(String testCaseFile) { this.testCaseFile = testCaseFile; }

    public List<String> getLanguage() { return language; }
    public void setLanguage(List<String> language) { this.language = language; }
}
