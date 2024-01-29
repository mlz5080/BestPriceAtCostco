import Image from "../nillkin-case-1.jpg";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

function ProductH(props) {
 
  return (
    <div className="col">
      <div className="card shadow-sm">
        <div className="row g-0">
          <div className="col-4">
            <Link to="/products/1" href="!#" replace>
              {/* {percentOff} */}
              <img
                className="rounded-start bg-dark cover w-100 h-100"
                alt=""
                src={props.product.product_image_link}
              />
            </Link>
          </div>
          <div className="col-8">
            <div className="card-body h-100">
              <div className="d-flex flex-column h-100">
                <h5 className="card-title text-dark text-truncate mb-1">
                  {props.product.product_name}
                </h5>
                <div>
                	<p className="text-center">Current Price ${props.product.product_current_price}</p>
          				<p className="text-center">History Minimum Price ${props.product.product_history_minimum_price}</p>
                </div>
                <div className="mt-auto d-flex">
                  <div className="d-grid gap-2">
				          	<span className="text-center text-muted small d-none d-md-inline">
				          		<a onClick={onClickUrl(props.product.product_link)} className="btn btn-outline-dark" replace>
				              Detail
				            </a>
				            <a className="btn btn-outline-dark" replace>
				              Interested
				            </a>
				          	</span>
				          </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductH;
export const openInNewTab = (url: string): void => {
	  const newWindow = window.open(url, '_blank', 'noopener,noreferrer')
	  if (newWindow) newWindow.opener = null
}

export const onClickUrl = (url: string): (() => void) => () => openInNewTab(url)