package com.exercise.soa.dto.request;

import com.exercise.soa.validation.OnCreate;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.*;
import lombok.Builder;
import lombok.Data;

import java.time.LocalDate;

@Data
@Builder
public class UserRequest {
    @NotNull(message = "Auth provider cannot be null", groups = OnCreate.class)
    private String authProvider;

    @NotNull(message = "Full name cannot be null", groups = OnCreate.class)
    @JsonProperty("fullName")
    private String fullName;

    @JsonProperty("username")
    private String username;

    @NotBlank(message = "Email cannot be empty", groups = OnCreate.class)
    @Email(message = "Invalid email format")
    private String email;

    private String bio;

    private String avatarUrl;

    @Past(message = "Date of birth must be in the past")
    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDate dateOfBirth;

    @Pattern(regexp = "^\\+?[0-9]{10,15}$", message = "Invalid phone number format")
    private String phoneNumber;

    private boolean darkMode;
}
