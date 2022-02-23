import { Component, OnInit } from '@angular/core';
import { RestServiceService } from '../services/rest-service.service';

@Component({
  selector: 'app-historial',
  templateUrl: './historial.page.html',
  styleUrls: ['./historial.page.scss'],
})
export class HistorialPage implements OnInit {

  proyectos:any[];
  constructor(public restService: RestServiceService) { }

  ngOnInit() {
  }

  ionViewWillEnter(){
    this.restService.getProyects()
    .then(data => {
      this.proyectos=data
      console.log(this.proyectos)
    });
  }
}
