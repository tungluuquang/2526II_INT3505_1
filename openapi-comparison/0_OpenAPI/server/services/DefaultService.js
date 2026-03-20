/* eslint-disable no-unused-vars */
const Service = require('./Service');

/**
* Lấy danh sách sách
*
* returns List
* */
const booksGET = () => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);
/**
* Xóa sách
*
* id String 
* no response value expected for this operation
* */
const booksIdDELETE = ({ id }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        id,
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);
/**
* Lấy chi tiết sách
*
* id String 
* returns Book
* */
const booksIdGET = ({ id }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        id,
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);
/**
* Cập nhật sách
*
* id String 
* bookInput BookInput 
* returns Book
* */
const booksIdPUT = ({ id, bookInput }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        id,
        bookInput,
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);
/**
* Thêm sách
*
* bookInput BookInput 
* returns Book
* */
const booksPOST = ({ bookInput }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        bookInput,
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);

module.exports = {
  booksGET,
  booksIdDELETE,
  booksIdGET,
  booksIdPUT,
  booksPOST,
};
