import FeatureProduct from "./FeatureProduct";
import ScrollToTopOnMount from "../template/ScrollToTopOnMount";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "react-router-dom";
import React, { useState, useEffect } from 'react';

function Landing(props) {
	const [featureProducts, setFeatureProducts] = useState([]);

	function get_random_feature_products() {
		fetch('/api/on_sale/random',{
	    headers:{
	        "accepts":"application/json"
	    }
		})
		.then(res => {
		    return res.json();
		})
		.then(json => {
			setFeatureProducts(json);
		})
		.catch( a => { console.log(a) })
	}

	useEffect(()=>{
    get_random_feature_products();
  }, [])

  return (
    <>
      <ScrollToTopOnMount />
      {/* <Banner /> */}
      <div className="d-flex flex-column bg-white py-4">
        <p className="text-center px-5">
        	<br />
        	<br />
          {/* Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do */}
          {/* eiusmod tempor incididunt ut labore et dolore magna aliqua. */}
        </p>
        <div className="d-flex justify-content-center">
          <Link 
	          style={{marginRight: "10px"}}
	          to="/products" className="btn btn-primary">
            Browse products
          </Link>
          <button onClick={(e) => get_random_feature_products()} className="btn btn-primary" >
            Refresh Feature Products
          </button>
        </div>
      </div>
      <h2 className="text-muted text-center mt-4 mb-3">Current On Sale items</h2>
      <div className="container pb-6 px-lg-5">
        <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 px-md-5">
        	{featureProducts.map((v, i) => {
            return <FeatureProduct product={v} key={i}/>;
          })}

          {/* {Array.from({ length: 6 }, (_, i) => { */}
          {/*   return <FeatureProduct product={i} />; */}
          {/* })} */}
        </div>
      </div>
      <div className="d-flex flex-column bg-white py-4">
        <h5 className="text-center mb-3">Follow me on</h5>
        <div className="d-flex justify-content-center">
          <a href="https://www.linkedin.com/in/ling-zhi-mo/" className="me-3">
            <FontAwesomeIcon icon={["fab", "linkedin"]} size="2x" />
          </a>
          <a href="https://github.com/mlz5080" className="me-3">
            <FontAwesomeIcon icon={["fab", "github"]} size="2x" />
          </a>
          {/* <a href="!#"> */}
          {/*   <FontAwesomeIcon icon={["fab", "instagram"]} size="2x" /> */}
          {/* </a> */}
          {/* <a href="!#" className="ms-3"> */}
          {/*   <FontAwesomeIcon icon={["fab", "twitter"]} size="2x" /> */}
          {/* </a> */}
        </div>
      </div>
    </>
  );
}

export default Landing;
