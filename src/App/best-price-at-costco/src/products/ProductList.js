import React, { useState, useEffect, useRef } from 'react';
import { Link } from "react-router-dom";
import Product from "./Product";
import ProductH from "./ProductH";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ScrollToTopOnMount from "../template/ScrollToTopOnMount";

function ProductList() {

  const [viewType, setViewType] = useState({ grid: true });
  const [onSaleProducts, setOnSaleProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [viewCategory, setViewCategory] = useState("View All");
  const [currentPage, setCurrentPage] = useState(1);

  let productRef = useRef([]);

  useEffect(()=>{
		fetch('/api/on_sale/categories',{
			headers:{
				"accepts":"application/json"
			}
		})
		.then(res => {
			return res.json();
		})
		.then(json => {
			json.unshift("View All");
			setCategories(json);
		})
		.catch( a => { console.log(a) });
  }, [])

  useEffect(()=>{
  	if (!productRef.current.length) {
	  	fetch('/api/on_sale/all',{
				headers:{
						"accepts":"application/json"
				}
			})
			.then(res => {
				return res.json();
			})
			.then(json => {
				productRef.current = json;
				setOnSaleProducts(productRef.current);
			})
			.catch( a => { console.log(a) });
		} else if (viewCategory === "View All") {
			setOnSaleProducts(productRef.current);
		} else {
			setOnSaleProducts(productRef.current.filter(product => 
				product.product_category == viewCategory)
			);	
		}
	}, [viewCategory])

  const usePagination = (items, setCurrentPage, page = 1, perPage = 9, ) => {
  	const [activePage, setActivePage] = useState(page)
  	const totalPages = Math.ceil(items.length / perPage)
  	const offset = perPage * (activePage - 1)
    const paginatedItems = items.slice(offset, perPage * activePage)
    if (page !== activePage) {
    	setActivePage(page);
    }
    return {
      activePage,
      nextPage: ()=> {setActivePage(p => p < totalPages ? p + 1 : p); window.scrollTo(0, 0); setCurrentPage(p => p < totalPages ? p + 1 : p)},
      previousPage: ()=> {setActivePage(p => p > 1 ? p - 1 : p); window.scrollTo(0, 0); setCurrentPage(p => p > 1 ? p - 1 : p)},
      totalPages,
      totalItems: items.length,
      items: paginatedItems
    }
  }

  const { activePage, nextPage, previousPage, totalPages, totalItems, items } = usePagination(onSaleProducts, setCurrentPage, currentPage);

  function changeViewType() {
    setViewType({
      grid: !viewType.grid,
    });
  }
  
  return (
    <div className="container mt-5 py-4 px-xl-5">
      <ScrollToTopOnMount />
      <nav aria-label="breadcrumb" className="bg-custom-light rounded">
        <ol className="breadcrumb p-3 mb-0">
          <li className="breadcrumb-item">
            <Link
              className="text-decoration-none link-secondary"
              to="/products"
              replace
            >
              All Prodcuts
            </Link>
          </li>
          <li className="breadcrumb-item active" aria-current="page">
            Cases &amp; Covers
          </li>
        </ol>
      </nav>

      <div className="h-scroller d-block d-lg-none">
        <nav className="nav h-underline">
          {categories.map((v, i) => {
            return (
              <div key={i} className="h-link me-2">
              	<button onClick={(e) => {setViewCategory(v); setCurrentPage(1); console.log(currentPage)}} className="btn btn-sm btn-outline-dark rounded-pill">{v}</button>
              </div>
            );
          })}
        </nav>
      </div>

      <div className="row mb-3 d-block d-lg-none">
        <div className="col-12">
          <div id="accordionFilter" className="accordion shadow-sm">
            <div className="accordion-item">
              <h2 className="accordion-header" id="headingOne">
                <button
                  className="accordion-button fw-bold collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#collapseFilter"
                  aria-expanded="false"
                  aria-controls="collapseFilter"
                >
                  Filter Products
                </button>
              </h2>
            </div>
            <div
              id="collapseFilter"
              className="accordion-collapse collapse"
              data-bs-parent="#accordionFilter"
            >
              <div className="accordion-body p-0">
                <FilterMenuLeft categories={categories} onViewCategoryChange={setViewCategory} resetCurrentPage={setCurrentPage} />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="row mb-4 mt-lg-3">
        <div className="d-none d-lg-block col-lg-3">
          <div className="border rounded shadow-sm">
            <FilterMenuLeft categories={categories} onViewCategoryChange={setViewCategory} resetCurrentPage={setCurrentPage} />
          </div>
        </div>
        <div className="col-lg-9">
          <div className="d-flex flex-column h-100">
            <div className="row mb-3">
              <div className="col-lg-3 d-none d-lg-block">
                {/* <select */}
                {/*   className="form-select" */}
                {/*   aria-label="Default select example" */}
                {/*   defaultValue="" */}
                {/* > */}
                {/*   <option value="">All Models</option> */}
                {/*   <option value="1">iPhone X</option> */}
                {/*   <option value="2">iPhone Xs</option> */}
                {/*   <option value="3">iPhone 11</option> */}
                {/* </select> */}
              </div>
              <div className="col-lg-9 col-xl-5 offset-xl-4 d-flex flex-row">
                <div className="input-group">
                  <input
                    id="filterProduct"
                    className="form-control"
                    type="text"
                    placeholder="Search products..."
                    aria-label="search input"
                  />
                  <button className="btn btn-outline-dark">
                    <FontAwesomeIcon icon={["fas", "search"]} />
                  </button>
                </div>
                <button
                  className="btn btn-outline-dark ms-2 d-none d-lg-inline"
                  onClick={changeViewType}
                >
                  <FontAwesomeIcon
                    icon={["fas", viewType.grid ? "th-list" : "th-large"]}
                  />
                </button>
              </div>
            </div>
            <div
              className={
                "row row-cols-1 row-cols-md-2 row-cols-lg-2 g-3 mb-4 flex-shrink-0 " +
                (viewType.grid ? "row-cols-xl-3" : "row-cols-xl-2")
              }
            >
            {items.map((v, i) => {
	            if (viewType.grid) {
                return (
                  <Product key={i} product={v} percentOff={i % 2 === 0 ? 15 : null} />
	                );
	              }
	              return (
	                <ProductH key={i} product={v} percentOff={i % 4 === 0 ? 15 : null} />
	              );
	          })}
            </div>
            <div className="d-flex align-items-center mt-auto">
              <span className="text-muted small d-none d-md-inline">
                Showing {activePage == totalPages ? totalItems : items.length*activePage} of {totalItems}
              </span>
              <nav aria-label="Page navigation example" className="ms-auto">
                <ul className="pagination my-0">
                  <li className="page-item">
                    <a className="page-link" onClick={previousPage} disabled={activePage <= 1}>
                      Previous
                    </a>
                  </li>
                  <li className="">
                    <div className="form-floating">
					            <input
					              id="pageInput"
					            	style={{width: "70px"}}
					              type="text"
					              className="form-control"
					              type="number"
					              min="1"
					              max={totalPages}
					              value={currentPage}
					              onWheel={(e) => e.target.blur()}
					              onChange={(e) => {
											    setCurrentPage(e.target.value);
				              		window.scrollTo(0, 0);
					              }}
					            />
					            <label htmlFor="pageInput">Go To</label>
					          </div>
                  </li>
                  <li className="page-item">
                    <a className="page-link" onClick={nextPage} disabled={activePage >= totalPages}>
                      Next
                    </a>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function FilterMenuLeft({categories, onViewCategoryChange, resetCurrentPage}) {

  return (
    <ul className="list-group list-group-flush rounded">
      <li className="list-group-item d-none d-lg-block">
        <h5 className="mt-1 mb-2">Browse</h5>
        <div className="d-flex flex-wrap my-2">
          {categories.map((v, i) => {
            return (
              <button
              	style = {{cursor: 'pointer'}}
              	onClick={(e) => {onViewCategoryChange(v); resetCurrentPage(1)}}
                key={i}
                className="btn btn-sm btn-outline-dark rounded-pill me-2 mb-2"
                >
                {v}
              </button>
            );
          })}
        </div>
      </li>
      {/* <li className="list-group-item"> */}
      {/*   <h5 className="mt-1 mb-2">Price Range</h5> */}
      {/*   <div className="d-grid d-block mb-3"> */}
      {/*     <div className="form-floating mb-2"> */}
      {/*       <input */}
      {/*         type="text" */}
      {/*         className="form-control" */}
      {/*         placeholder="Min" */}
      {/*         defaultValue="100000" */}
      {/*       /> */}
      {/*       <label htmlFor="floatingInput">Min Price</label> */}
      {/*     </div> */}
      {/*     <div className="form-floating mb-2"> */}
      {/*       <input */}
      {/*         type="text" */}
      {/*         className="form-control" */}
      {/*         placeholder="Max" */}
      {/*         defaultValue="500000" */}
      {/*       /> */}
      {/*       <label htmlFor="floatingInput">Max Price</label> */}
      {/*     </div> */}
      {/*     <button className="btn btn-dark">Apply</button> */}
      {/*   </div> */}
      {/* </li> */}
    </ul>
  );
}

export default ProductList;
