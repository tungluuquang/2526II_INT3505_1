package com.exercise.soa.service;

import com.exercise.soa.advice.ExceptionControllerAdvice;
import com.exercise.soa.dto.request.UserRequest;
import com.exercise.soa.dto.response.UserResponse;
import com.exercise.soa.mapper.UserMapper;
import com.exercise.soa.model.User;
import com.exercise.soa.repository.UserRepository;
import lombok.AllArgsConstructor;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.NoSuchElementException;

@Service
@AllArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final UserMapper userMapper;
    public User findEntityById(String id) {
        return userRepository.findById(id).orElseThrow(() ->
                new NoSuchElementException("No such user with id " + id));
    }

    public UserResponse findById(String id) {
        return userMapper.toResponse(this.findEntityById(id));
    }

    public UserResponse getUserResponseById(String id) {
        UserResponse user = findById(id);
        return user;
    }

    public UserResponse create(UserRequest userRequest) {
        User user = User.builder()
                .email(userRequest.getEmail())
                .fullName(userRequest.getFullName())
                .username(userRequest.getUsername())
                .authProvider(userRequest.getAuthProvider())
                .bio(userRequest.getBio())
                .avatarUrl(userRequest.getAvatarUrl())
                .dateOfBirth(userRequest.getDateOfBirth())
                .phoneNumber(userRequest.getPhoneNumber())
                .isDarkMode(userRequest.isDarkMode())
                .build();

        User savedUser = userRepository.save(user);
        return userMapper.toResponse(savedUser);
    }

    public UserResponse update(String userId, UserRequest userRequest) throws AccessDeniedException {
        User existedUser = this.findEntityById(userId);
        if (userRequest.getBio() != null) {
            existedUser.setBio(userRequest.getBio());
        }
        if (userRequest.getAvatarUrl() != null) {
            existedUser.setAvatarUrl(userRequest.getAvatarUrl());
        }
        if (userRequest.getDateOfBirth() != null) {
            existedUser.setDateOfBirth(userRequest.getDateOfBirth());
        }
        if (userRequest.getPhoneNumber() != null) {
            existedUser.setPhoneNumber(userRequest.getPhoneNumber());
        }

        if (userRequest.isDarkMode()) {
            existedUser.setDarkMode(true);
        } else {
            existedUser.setDarkMode(false);
        }
        return userMapper.toResponse(userRepository.save(existedUser));
    }

    public void delete(String userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new NoSuchElementException("User not found with id: " + userId));

        userRepository.delete(user);
    }

    public boolean existsById(String userId) {
        return userRepository.existsById(userId);
    }

    public List<UserResponse> findAllUsers() {
        return userRepository.findAll()
                .stream()
                .map(userMapper::toResponse)
                .toList();
    }
}
