import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RestServiceService {
  apiUrl = 'http://127.0.0.1:8000/api';
  data_user:any;
  constructor(private http: HttpClient) { }


  async login(username, password) {
    return await new Promise<any>(resolve => {
      this.http.post(this.apiUrl + '/login',
        {
          user: username,
          password: password
        })
        .subscribe(data => {
          this.data_user = data;
          console.log(this.data_user);
          resolve(data);
        }, err => {
          console.log(err);
        });
    });
  }
  async getProyects() {
    console.log(this.data_user.token)
    return await new Promise<any>(resolve => {

      this.http.get(this.apiUrl + '/Historial', {
        headers: new HttpHeaders().set('Authorization', 'Token ' + this.data_user.token),
      })
        .subscribe(data => {
          console.log(data)
          resolve(data);
        }, err => {
          console.log(err);
        });
    });
  }

}