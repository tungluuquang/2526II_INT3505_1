export interface Book {
  id: string;
  title: string;
  author: string;
}

export interface BookInput {
  title: string;
  author: string;
}

export interface Error {
  message: string;
}

export class LibraryClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async getBooks(): Promise<Book[]> {
    const res = await fetch(`${this.baseUrl}/books`);
    return res.json();
  }

  async addBook(payload: BookInput): Promise<Book> {
    const res = await fetch(`${this.baseUrl}/books`, {
      method: 'POST',
      body: JSON.stringify(payload)
    });
    return res.json();
  }

  async getBookById(id: string): Promise<Book> {
    const res = await fetch(`${this.baseUrl}/books/${id}`);
    if (res.status === 404) throw new Error("Not Found");
    return res.json();
  }
}