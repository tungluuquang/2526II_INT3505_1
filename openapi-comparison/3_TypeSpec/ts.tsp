import "@typespec/http";
import "@typespec/rest";

using Http;
using Rest;

@service(#{ title: "Library API (Simple)" })
@server("http://localhost:3000/api", "Cổng API chính")
namespace Library;

// --- Data Structures ---

model Book {
  id: string;
  title: string;
  author: string;
}

model BookInput {
  title: string;
  author: string;
}

model Member {
  id: string;
  name: string;
}

model Loan {
  id: string;
  bookId: string;
  memberId: string;
}

model Error {
  message: string;
}

// --- API Endpoints ---

@route("/books")
@tag("Books")
interface Books {

  @doc("Lấy danh sách sách")
  @get list(): Book[];

  @doc("Thêm sách mới")
  @post create(@body book: BookInput): Book & { @statusCode statusCode: 201 };

  @doc("Lấy chi tiết sách")
  @get @route("/{id}")
  read(@path id: string): Book | (Error & { @statusCode statusCode: 404 });

  @doc("Xóa sách")
  @delete @route("/{id}")
  delete(@path id: string): 
    { @statusCode statusCode: 204 } |
    (Error & { @statusCode statusCode: 404 });
}

@route("/members")
@tag("Members")
interface Members {

  @doc("Lấy danh sách thành viên")
  @get list(): Member[];

  @doc("Tạo thành viên mới")
  @post create(@body member: Member): Member & { @statusCode statusCode: 201 };
}

@route("/loans")
@tag("Loans")
interface Loans {

  @doc("Mượn sách")
  @post create(@body loan: Loan): Loan & { @statusCode statusCode: 201 };
}