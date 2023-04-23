import {
  Component,
  ElementRef,
  HostListener,
  Input,
  OnInit,
  ViewChild,
} from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { fadeIn, fadeInOut } from '../animations';
import { EventEmitter } from '@angular/core';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'chat-widget',
  templateUrl: './chat-widget.component.html',
  styleUrls: ['./chat-widget.component.scss'],
  animations: [fadeInOut, fadeIn],
})
export class ChatWidgetComponent implements OnInit {
  @ViewChild('bottom') bottom: ElementRef;
  @Input() public theme: 'blue';
  nameRegex = /^[A-Z][a-z]+(\s[A-Z][a-z]+)*$/;
  emailRegex = /\S+@\S+\.\S+/;
  public _visible = false;

  public _displayButtons: boolean = false;

  answer: string = 'default answer';
  constructor(private chatService: ChatService) {}

  public get visible() {
    return this._visible;
  }

  @Input() public set visible(visible) {
    this._visible = visible;
    if (this._visible) {
      setTimeout(() => {
        this.scrollToBottom();
        this.focusMessage();
      }, 0);
    }
  }

  public focus = new EventEmitter<any>();

  // https://randomuser.me/api/portraits/men/${rand(100)}.jpg    --- Use this if you want to display user images
  public operator = {
    name: 'HealthBot',
    status: 'Online',
    avatar: `../../../assets/istockphoto.jpg`,
  };

  public client = {
    name: 'Guest User',
    status: 'online',
    avatar: `../../../assets/istockphoto.jpg`,
  };

  dataTobeSent: string = '';

  public messages: Array<{
    from: string;
    text: string;
    intent: string;
    type: 'received' | 'sent';
    date: number;
  }> = [];

  public addMessage(from, text, intent, type: 'received' | 'sent' ) {
    this.messages.unshift({
      from,
      text,
      intent,
      type,
      date: new Date().getTime(),
    });
    this.scrollToBottom();
  }

  public scrollToBottom() {
    if (this.bottom !== undefined) {
      this.bottom.nativeElement.scrollIntoView();
    }
  }

  public focusMessage() {
    this.focus.next(true);
  }

  public getResponseMessage(message) {
    const mostRecentMessage = this.messages.find(
      (message) => message.type === 'received'
    );
    if (mostRecentMessage?.intent === 'name') {
        this.dataTobeSent = message;
        this.answer = 'Please enter your email';
        this.addMessage(this.operator, this.answer, 'email', 'received');
        return;
      }
      if (this.emailRegex.test(message) && mostRecentMessage?.intent === 'email') {
        this.dataTobeSent = this.dataTobeSent + '<' + message;
        this.answer =
          'Please enter your symptoms separated by comma (ex: fever, cough))';
        this.addMessage(this.operator, this.answer, 'symptoms', 'received');
        return;
      }
    if (mostRecentMessage?.intent === 'symptoms') {
      this.dataTobeSent = this.dataTobeSent + '<' + message.replace(/,\s*/g, '|').replace(/\s+/g, '');
      message = this.dataTobeSent;
    }
    this.chatService.postChatData(message).subscribe((data) => {
      if (data.intent === 'BookAppointment') {
        this.answer = 'Please enter your name';
        this.addMessage(this.operator, this.answer, 'name', 'received');
        return;
      }
      this.answer = data.answers[data.answers.length - 1];
      this.addMessage(this.operator, this.answer, data.intent, 'received');
    });
  }

  ngOnInit() {
    setTimeout(() => (this.visible = true), 1000);
    setTimeout(() => {
      this.addMessage(
        this.operator,
        `<bold>This chatbot is not a substitute for professional medical advice, diagnosis, or treatment. If you have a medical emergency, please seek immediate help from a healthcare provider.</bold>`,
        'inital',
        'received'
      );
    }, 1500);
    setTimeout(() => {
      this.addMessage(
        this.operator,
        'I can help you to <br/> 1. Book Appointment <br/> 2. Reschedule Appointment  <br/> 3. Cancel Appointment <br/><br/>',
        'inital',
        'received'
      );
    }, 2500);
    setTimeout(() => {
      this.addMessage(
        this.operator,
        'Hi, How can I help you today?',
        'initial',
        'received'
      );
    }, 3500);

    console.log(this.messages);
  }

  public toggleChat() {
    this.visible = !this.visible;
  }

  public sendMessage({ message }) {
    if (message.trim() === '') {
      return;
    }
    console.log(message);
    this.addMessage(this.client, message, '', 'sent');
    setTimeout(() => this.getResponseMessage(message), 1000);
  }

  @HostListener('document:keypress', ['$event'])
  handleKeyboardEvent(event: KeyboardEvent) {
    if (event.key === '/') {
      this.focusMessage();
    }
    if (event.key === '?' && !this._visible) {
      this.toggleChat();
    }
  }
}
