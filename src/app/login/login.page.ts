import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { RestServiceService } from '../services/rest-service.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {
  username= new FormControl('');
  password = new FormControl('');
  datoslog: any;
  constructor(public restService: RestServiceService, private router: Router) { }
 

  ngOnInit() {
  }

  login(){
    console.log(this.username)
    this.restService.login(this.username.value, this.password.value)
    .then(data => {
      this.datoslog = data.Token;

      if(this.datoslog=!null){
        this.router.navigate(['historial'])
  
      }
    });
    
  }

}
