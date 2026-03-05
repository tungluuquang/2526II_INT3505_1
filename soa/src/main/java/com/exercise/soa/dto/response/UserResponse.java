package com.exercise.soa.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.List;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class UserResponse {
    private String id;
    private String fullName;
    private String email;
    private String authProvider;
    private String bio;
    private String avatarUrl;
    private LocalDate dateOfBirth;
    private String phoneNumber;
    private List<String> skills;
    private boolean darkMode;
}
