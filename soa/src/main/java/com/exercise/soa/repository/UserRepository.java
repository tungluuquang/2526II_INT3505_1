package com.exercise.soa.repository;

import com.exercise.soa.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface UserRepository extends JpaRepository<User, String> {
    Optional<User> findByEmail(String email);

    @Query("""
    select u from User u
    where u.id in :userIds
    """)
    List<User> findAllByIds(@Param("userIds") List<String> userIds);

}
