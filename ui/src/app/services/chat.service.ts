import { Injectable } from '@angular/core';
import { Observable, throwError, Subject } from 'rxjs';
import { first, map, retry , tap} from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { ChatConversation } from '../models/chatconversations';
import { environment } from 'src/environments/environment';
@Injectable({
  providedIn: 'root',
})
export class ChatService {
  constructor(private http: HttpClient) {}
  conversation = new ChatConversation();

  serverResponse: string = '';

  postChatData(question: string): Observable<ChatConversation> {
    if (!this.conversation) {
      this.conversation = new ChatConversation();
    }
    this.conversation.question = question;
    return this.http
      .post<any>(environment.apiUrl, this.conversation) // chnage this value to question from the parameter passed to this method
      .pipe(
        tap((data) => {
          this.conversation.addResponse(data);
        }),
        map(() => this.conversation)
      );
  }
}
