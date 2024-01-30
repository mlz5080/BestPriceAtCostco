import React from 'react';
import { onClickUrl } from "../Utils"

function Product(props) {

  return (
    <div className="col">
      <div className="card shadow-sm">
        <div onClick={onClickUrl(props.product.product_link)} >
          <img
            className="card-img-top bg-dark cover"
            alt=""
            src={props.product.product_image_link}
          />
        </div>
        <div className="card-body">
          <h6 className="card-title text-center text-dark text-truncate">
            {props.product.product_name}
          </h6>
          <div>
          	<p className="text-center">Current Price ${props.product.product_current_price}</p>
    				<p className="text-center">History Minimum Price ${props.product.product_history_minimum_price}</p>
          </div>
          <div className="mt-auto text-center">
            <div className="d-grid gap-2">
	          	<span className="text-center text-muted">
	          		<button style={{marginRight: "10px"}} onClick={onClickUrl(props.product.product_link)} className="btn btn-outline-dark" >
	              	Detail
	            	</button>
		            <button className="btn btn-outline-dark" >
		              Interested
		            </button>
          		</span>
	          </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Product;