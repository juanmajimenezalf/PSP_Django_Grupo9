import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators, FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { AlertController } from '@ionic/angular';
import { RestServiceService } from '../services/rest-service.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {
  
  datoslog: any;
  formularioLogin: FormGroup;

  constructor(public restService: RestServiceService, private router: Router, public fb: FormBuilder, public alertControler: AlertController) { 
    this.formularioLogin = this.fb.group({
      'username': new FormControl("", Validators.required),
      'password': new FormControl("", Validators.required)
    })
  }
  
  

  ngOnInit() {
  }

  async login(){

    if(this.formularioLogin.invalid){
      const alert = await this.alertControler.create({
        header: 'Fallo al iniciar sesion',
        message: 'Datos incompletos',
        buttons: ['Aceptar'],
      });
      await alert.present();
      return;
    }
    
    
    this.restService.login(this.formularioLogin.value.username, this.formularioLogin.value.password)
    .then(data => {
      this.datoslog = data.Token;

      if(this.datoslog=!null){
        this.router.navigate(['historial'])
      }
    }
    );
    
  }

}
