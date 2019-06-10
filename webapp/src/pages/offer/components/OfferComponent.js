import React, {Component} from "react";
import {withRouter} from "react-router";
import TextArea from "react";
import {Chart} from "react-google-charts";
import { offerServices  } from "../../../services/offer/offer.service";

const DEFAULT_EVENT_ID = process.env.REACT_APP_DEFAULT_EVENT_ID || 1;

class Offer extends Component {
  
  constructor(props) {
        super(props);
  
        this.state = {
          loading: true,
          error: "",
          offer_id: 1,
          rejected_reason:"",
          rejected:false,
          accepted: false,
          offerList: [],
          category:""
        };
      }
    

      handleChange = field => {
        return event => {
          this.setState({
            [field.name]: event.target.value
          });
        };
      };

      buttonSubmit(event){
        event.preventDefault();
        let offer_id=0,
         accepted=false, 
         rejected=false, 
         rejected_reason='';

        offerServices.updateOfferList(offer_id, DEFAULT_EVENT_ID, accepted, rejected, rejected_reason)
        .then(response=>{
          if (response.msg === "succeeded") {
            this.getofferList();
            this.setState({
              addedSucess: true,
              conflict: false,
              notFound: false
            });
          } else if (response.msg === "404") {
            this.setState({
              addedSucess: false,
              notFound: true,
              conflict: false
            });
          } else if (response.msg === "409") {
            this.setState({
              notFound: false,
              addedSucess: false,
              conflict: true
            });
          }
        })
      }
    
    displayOfferContent = () => {
      const {offerList} = this.state;
     return(   
      <div className="container"  align="center" >
      <p className="h5 pt-5">We are pleased to offer you a place at the Deep Learning Indaba 2019. Please see the details of this offer below </p>

      <form class="pt-5">
        <p>You have been accepted as a  {offerList!=null ? this.state.category: "<Category>"} </p>
        <p>Your status</p>
        <div class="row">
          <div class="col-8">
            Travel Award:
          </div>
          <div class="col-2">
          {offerList!=null
          ? offerList.travel_award
          : "Not avaiable"}
          </div>
        </div>

        <div class="row">
          <div class="col-8">
            Accommodation Award:
          </div>
          <div class="col-2">
          {offerList!=null
          ? offerList.accomodation_award
          : "Not avaiable"}
          </div>
        </div>

        <div class="row pb-5">
          <div class="col-8">
            Payment Required:
          </div>
          <div class="col-2">
          {offerList!=null
          ? offerList.payment_required
          : "Not avaiable"}
          </div>
        </div>
        <p>Please accept or reject this offer by {offerList!=null ? offerList.expiry_date : "<Expirery Date>"} </p>
        <div class="row">
         <div class="col">
          <button class="btn btn-danger" id="reject"onClick={
            ()=>{
              this.setState({
                rejected:true
              });
              this.buttonSubmit();
            }
          } >
              Reject
          </button>
          </div>
          <div class="col">
          <button class="btn btn-success" id="accept" onClick={()=>{
              this.setState({
                accepted:true,
                rejected:false,
              });
              this.buttonSubmit();
          }}>
              Accept
          </button>
          </div>
        </div> 

        <div class="form-group">
         { this.state.rejected ? 
          <div class="form-group mr-5  ml-5 pt-5" >
          <textarea class="form-control pr-5 pl-10" id="exampleFormControlTextarea3" onChange={()=>{this.handleChange(this.rejected_reason)}}  placeholder="Enter rejection message"></textarea>
        </div>
        :""}
        </div>
      
      </form>
  </div>
      )}

    componentDidMount() {
      console.log("### - ",this.state.rejected,"%%%%%",this.state.accepted)
          this.getOfferList();  
          this.setState({
            loading: false,
            buttonLoading: false
          });
      }
   
      getOfferList (){
        this.setState({loading:true});
        offerServices.getOfferList(DEFAULT_EVENT_ID).then(result => {
          this.setState({
            loading:false,
            offerList:result.form,
            error:result.error
          });
        });
      }
      
    render(){
      const {loading, offerList, error} = this.state;

      const loadingStyle = {
        "width": "3rem",
        "height": "3rem"
      }

      if (loading) {
        return (
          <div class="d-flex justify-content-center pt-5">
            <div class="spinner-border" style={loadingStyle} role="status">
              <span class="sr-only">Loading...</span>
            </div>
          </div>
        )
      }

      // if (error) 
      //   return <div class="alert alert-danger" align="center">{error}</div>
      // else 
        if (offerList!=null) 
          return <div className="h5 pt-5" align="center"> You are currently on the waiting list for the Deep Learning Indaba 2019. Please await further communication</div>
        else
          return this.displayOfferContent();
        

    }
}

export default withRouter(Offer);