package com.competa_arena.contest_service.services;

import com.competa_arena.contest_service.dtos.ContestRequestDto;
import com.competa_arena.contest_service.dtos.QuestionDto;
import com.competa_arena.contest_service.entities.Contest;
import com.competa_arena.contest_service.entities.Question;
import com.competa_arena.contest_service.repositories.ContestRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Service
public class ContestService {

    @Autowired
    private ContestRepository contestRepository;

    @Autowired
    private FileService fileService;

    public Contest createContest(ContestRequestDto dto, String createdBy) throws IOException {
        validateContest(dto);

        List<Question> questions = new ArrayList<>();

        for (QuestionDto qDto : dto.getQuestions()) {
            Question question = mapQuestion(qDto);
            
            if ("PROGRAMMING".equalsIgnoreCase(qDto.getType())) {
                String statementUrl = fileService.uploadFile(qDto.getStatementMultipart(), "contests/programming");
                String testCaseUrl = fileService.uploadFile(qDto.getTestCaseMultipart(), "contests/programming");
                question.setStatementFile(statementUrl);
                question.setTestCaseFile(testCaseUrl);
                question.setLanguage(qDto.getLanguage());
            }

            questions.add(question);
        }

        Contest contest = new Contest();
        contest.setTitle(dto.getTitle());
        contest.setSubject(dto.getSubject());
        contest.setVisibility(dto.getVisibility());
        contest.setCreatedBy(createdBy);
        contest.setQuestions(questions);
        contest.setStartTime(dto.getStartTime());
        contest.setEndTime(dto.getEndTime());

        return contestRepository.save(contest);
    }

    public List<Contest> getAllContests() {
        return contestRepository.findAll();
    }

    public Contest getContestById(String id) {
        return contestRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Contest not found"));
    }

    public void deleteContest(String id) {
        contestRepository.deleteById(id);
    }

    public Contest updateContest(String id, ContestRequestDto dto) throws IOException {
        Contest existing = getContestById(id);
        validateContest(dto);

        List<Question> questions = new ArrayList<>();
        for (QuestionDto qDto : dto.getQuestions()) {
            Question question = mapQuestion(qDto);

            if ("PROGRAMMING".equalsIgnoreCase(qDto.getType())) {
                String statementUrl = fileService.uploadFile(qDto.getStatementMultipart(), "contests/programming");
                String testCaseUrl = fileService.uploadFile(qDto.getTestCaseMultipart(), "contests/programming");
                question.setStatementFile(statementUrl);
                question.setTestCaseFile(testCaseUrl);
                question.setLanguage(qDto.getLanguage());
            }

            questions.add(question);
        }

        existing.setTitle(dto.getTitle());
        existing.setSubject(dto.getSubject());
        existing.setVisibility(dto.getVisibility());
        existing.setQuestions(questions);
        existing.setStartTime(dto.getStartTime());
        existing.setEndTime(dto.getEndTime());

        return contestRepository.save(existing);
    }

    private void validateContest(ContestRequestDto dto) {
        if ((dto.getSubject().equalsIgnoreCase("Math") || dto.getSubject().equalsIgnoreCase("Physics"))
                && dto.getQuestions().stream().anyMatch(q -> q.getType().equalsIgnoreCase("PROGRAMMING"))) {
            throw new IllegalArgumentException("Math and Physics contests cannot have programming questions");
        }

        if (dto.getSubject().equalsIgnoreCase("ComputerScience")) {
            // ComputerScience can have all types
        }
    }

    private Question mapQuestion(QuestionDto qDto) {
        Question question = new Question();
        question.setType(qDto.getType());
        question.setQuestion(qDto.getQuestion());

        if ("MCQ".equalsIgnoreCase(qDto.getType())) {
            question.setOptions(qDto.getOptions());
            question.setAnswer(qDto.getAnswer());
        } else if ("SHORT_ANSWER".equalsIgnoreCase(qDto.getType())) {
            question.setExpectedAnswer(qDto.getExpectedAnswer());
        }

        return question;
    }
}
