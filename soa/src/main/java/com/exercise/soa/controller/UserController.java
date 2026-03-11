package com.exercise.soa.controller;

import com.exercise.soa.dto.request.UserRequest;
import com.exercise.soa.dto.response.UserResponse;
import com.exercise.soa.service.UserService;
import com.exercise.soa.validation.OnCreate;
import com.exercise.soa.validation.OnUpdate;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/users/users")
@AllArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping("/{userId}")
    public ResponseEntity<UserResponse> findById(@PathVariable String userId) {
        return ResponseEntity.ok(userService.findById(userId));
    }

    @PostMapping
    public ResponseEntity<UserResponse> create(@Validated(OnCreate.class) @RequestBody UserRequest userRequest) {
        return new ResponseEntity<>(userService.create(userRequest), HttpStatus.CREATED);
    }

    @PatchMapping("/{userId}")
    public ResponseEntity<UserResponse> update(
            @PathVariable String userId,
            @Validated(OnUpdate.class) @RequestBody UserRequest userRequest) {
        return new ResponseEntity<>(userService.update(userId, userRequest), HttpStatus.OK);
    }

    @DeleteMapping("/{userId}")
    public ResponseEntity<?> deleteUser(@PathVariable String userId) {
        if (!userService.existsById(userId)) {
            return ResponseEntity.notFound().build();
        }

        userService.delete(userId);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/all-users")
    public ResponseEntity<List<UserResponse>> allUsers() {
        return ResponseEntity.ok(userService.findAllUsers());
    }

    @GetMapping("/error")
    public ResponseEntity<String> getError() {
        throw new RuntimeException("Something went wrong on the server");
    }

}
