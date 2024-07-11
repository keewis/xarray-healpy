def classify_grid(ds):
    # strategy:
    # - find horizontal coords using cf-xarray
    # - classify based on dimensions:
    #   * 1D with different dimensions: 1D rectilinear
    #   * 2D with constant values along one dimension: 2D rectilinear
    #   * 2D with varying values along all dimensions: 2D curvilinear
    #   * 1D with identical dimensions: unstructured
    pass
