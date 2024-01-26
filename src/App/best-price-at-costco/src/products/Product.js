import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import axios from "axios";

function Product(props) {
	const [product, setProduct] = useState(0);
  let percentOff;

  useEffect(()=>{
  	fetch('/api/product_id/1000092',{
	    headers:{
	        "accepts":"application/json"
	    }
		})
		.then(res => {
		    console.log(res);
		    return res.json();
		})
		.then(json => {
			console.log(json);
			setProduct(json);
		})
		.catch( a => { console.log(a) });
  }, [])

  return (
    <div className="col">
      <div className="card shadow-sm">
        <Link to="/products/1000092" href="!#" replace>
          {product.product_name}
          <img
            className="card-img-top bg-dark cover"
            height="200"
            alt=""
            src={product.product_image_link}
          />
        </Link>
        <div className="card-body">
          <h5 className="card-title text-center text-dark text-truncate">
            {product.product_name}
          </h5>
          <p className="card-text text-center text-muted mb-0">{product.product_current_price}</p>
          <div className="d-grid d-block">
            <button className="btn btn-outline-dark mt-3">
              <FontAwesomeIcon icon={["fas", "cart-plus"]} /> Add to cart
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Product;
