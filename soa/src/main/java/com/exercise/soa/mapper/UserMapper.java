package com.exercise.soa.mapper;

import com.exercise.soa.dto.response.UserResponse;
import com.exercise.soa.model.User;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class UserMapper {

    public UserResponse toResponse(User user) {
        if (user == null) {
            return null;
        }

        return UserResponse.builder()
                .id(user.getId())
                .authProvider(user.getAuthProvider())
                .fullName(user.getFullName())
                .email(user.getEmail())
                .avatarUrl(user.getAvatarUrl())
                .bio(user.getBio())
                .avatarUrl(user.getAvatarUrl())
                .skills(user.getSkills())
                .dateOfBirth(user.getDateOfBirth())
                .phoneNumber(user.getPhoneNumber())
                .darkMode(user.isDarkMode())
                .build();
    }

}
