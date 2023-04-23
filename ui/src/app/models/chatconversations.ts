export class ChatConversation {
  public answers: string[] = [];
  public intent: string = '';
  public previous_questions: string[] = [];
  public question: string = '';

    public addResponse(response: any) {
      this.answers = this.answers.concat(response.answers);
      this.intent = response.intent;
      this.previous_questions = response.previous_questions;
    }

  }

  