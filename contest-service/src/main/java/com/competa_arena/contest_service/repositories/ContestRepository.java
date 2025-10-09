package com.competa_arena.contest_service.repositories;

import com.competa_arena.contest_service.entities.Contest;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ContestRepository extends MongoRepository<Contest, String> {

    // Find all contests for a specific subject
    List<Contest> findBySubject(String subject);

    // Find all contests created by a specific user
    List<Contest> findByCreatedBy(String userId);

    // Optional: Find all public contests
    List<Contest> findByVisibility(String visibility);
}
