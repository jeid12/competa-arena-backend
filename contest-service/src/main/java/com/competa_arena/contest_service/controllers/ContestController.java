package com.competa_arena.contest_service.controllers;

import com.competa_arena.contest_service.dtos.ContestRequestDto;
import com.competa_arena.contest_service.entities.Contest;
import com.competa_arena.contest_service.services.ContestService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/contests")
public class ContestController {

    @Autowired
    private ContestService contestService;

    /**
     * Create a new contest (Only CREATOR or ADMIN allowed via JWT filter)
     */
    @PostMapping(consumes = "application/json")
    public ResponseEntity<Contest> createContest(
            @RequestBody ContestRequestDto contestDto,
            HttpServletRequest request
    ) throws IOException {

        // Extract userId from JWT filter (set in filter)
        String createdBy = (String) request.getAttribute("userId");

        // Service handles Cloudinary file upload internally if needed
        Contest createdContest = contestService.createContest(contestDto, createdBy);
        return ResponseEntity.ok(createdContest);
    }

    /**
     * Get all contests
     */
    @GetMapping
    public ResponseEntity<List<Contest>> getAllContests() {
        List<Contest> contests = contestService.getAllContests();
        return ResponseEntity.ok(contests);
    }

    /**
     * Get contest by ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<Contest> getContestById(@PathVariable String id) {
        Contest contest = contestService.getContestById(id);
        return ResponseEntity.ok(contest);
    }

    /**
     * Update contest by ID (Only CREATOR or ADMIN)
     */
    @PutMapping(value = "/{id}", consumes = "application/json")
    public ResponseEntity<Contest> updateContest(
            @PathVariable String id,
            @RequestBody ContestRequestDto contestDto,
            HttpServletRequest request
    ) throws IOException {

        String updatedBy = (String) request.getAttribute("userId");
        Contest updatedContest = contestService.updateContest(id, contestDto);
        return ResponseEntity.ok(updatedContest);
    }

    /**
     * Delete contest by ID (Only CREATOR or ADMIN)
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteContest(@PathVariable String id) {
        contestService.deleteContest(id);
        return ResponseEntity.noContent().build();
    }
}
