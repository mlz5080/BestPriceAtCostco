function FeatureProduct({product}) {

	const openInNewTab = (url: string): void => {
	  	const newWindow = window.open(url, '_blank', 'noopener,noreferrer')
	  	if (newWindow) newWindow.opener = null
	}

	const onClickUrl = (url: string): (() => void) => () => openInNewTab(url)

  return (
    <div className="col">
      <div className="card shadow-sm">
        <img
          className="card-img-top bg-dark cover"
          object-fit="scale-down"
          alt=""
          src={product.product_image_link}
        />
        <div className="card-body">
          <h5 className="card-title text-center">{product.product_name}</h5>
          <p className="card-text text-center text-muted">Current Price ${product.product_current_price}</p>
          <p className="card-text text-center text-muted">History Minimum Price ${product.product_history_minimum_price}</p>
          <div className="d-grid gap-2">
          	<span className="text-center text-muted">
          		<button style={{marginRight: "10px"}} onClick={onClickUrl(product.product_link)} className="btn btn-outline-dark" replace>
              	Detail
            	</button>
	            <button className="btn btn-outline-dark" replace>
	              Interested
	            </button>
          	</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default FeatureProduct;