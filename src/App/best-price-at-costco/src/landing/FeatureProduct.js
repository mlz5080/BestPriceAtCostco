import { onClickUrl } from "../Utils"

function FeatureProduct({product}) {

  return (
  	<div className="col">
      <div className="card shadow-sm">
        <div onClick={onClickUrl(product.product_link)} >
          <img
            className="card-img-top bg-dark cover"
            alt=""
            src={product.product_image_link}
          />
        </div>
        <div className="card-body">
          <h6 className="card-title text-center text-dark text-truncate">
            {product.product_name}
          </h6>
          <div>
          	<p className="text-center">Current Price ${product.product_current_price}</p>
    				<p className="text-center">History Minimum Price ${product.product_history_minimum_price}</p>
          </div>
          <div className="mt-auto text-center">
            <div className="d-grid gap-2">
	          	<span className="text-center text-muted">
	          		<button style={{marginRight: "10px"}} onClick={onClickUrl(product.product_link)} className="btn btn-outline-dark" >
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

export default FeatureProduct;