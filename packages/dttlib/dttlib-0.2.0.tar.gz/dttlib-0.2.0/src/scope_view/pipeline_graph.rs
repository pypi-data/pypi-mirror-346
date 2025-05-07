//! Create pipeline graph for a ScopeView

use crate::analysis::graph::analysis::{create_analysis_graph, test_schemes, AnalysisGraph};
use crate::analysis::graph::scheme::{SchemeEdge, SchemeGraph, SchemeNode, SchemePipelineType};
use crate::analysis::result::EdgeResultsWrapper;
use crate::errors::DTTError;
use crate::run_context::RunContext;
use crate::scope_view::ScopeView;


pub fn create_pipeline_graph<'b>(rc: Box<RunContext>, view: &ScopeView) -> Result<AnalysisGraph<'b>, DTTError> {

    // Because we aren't handling functions yet, we can just hook data source to results
    // and pass it as a per-channel graph
    // When arbitrary functions are allowed on individual channels, then
    // Some more involved method will be needed.

    let mut scheme = SchemeGraph::new();

    let ds_index = scheme.add_node(
        SchemeNode::new("data_source", SchemePipelineType::DataSource));
    
    let condition_index = scheme.add_node(SchemeNode::new("conditioning", SchemePipelineType::Conditioning));

    //let splice_index = scheme.add_node(SchemeNode::new("splice", SchemePipelineType::Splice));

    let results_index = scheme.add_node(SchemeNode::new("results",
                                                        SchemePipelineType::Results));
    
    let downsample_index = scheme.add_node(SchemeNode::new("downsample", SchemePipelineType::Downsample));
    
    let fft_index = scheme.add_node(SchemeNode::new("fft", SchemePipelineType::InlineFFT));
    let csd_index = scheme.add_node(SchemeNode::new("csd", SchemePipelineType::CSD));
    let real_index = scheme.add_node(SchemeNode::new("real", SchemePipelineType::Real));
    let avg_index = scheme.add_node(SchemeNode::new("avg", SchemePipelineType::Average));
    let sqrt_index = scheme.add_node(SchemeNode::new("sqrt", SchemePipelineType::Sqrt));



    scheme.add_edge(ds_index, condition_index, SchemeEdge::new(1));
    
    // scheme.add_edge(condition_index, splice_index, SchemeEdge::new(1));
    // scheme.add_edge(splice_index, results_index, SchemeEdge::new(1));
    
    scheme.add_edge(condition_index, downsample_index, SchemeEdge::new(1));
    scheme.add_edge(downsample_index, results_index, SchemeEdge::new(1).set_result_wrapper(EdgeResultsWrapper::TimeDomainReal));
    
    //scheme.add_edge(condition_index, results_index, SchemeEdge::new(1));

    // hook up ASD calc
    scheme.add_edge(condition_index, fft_index, SchemeEdge::new(1));

    // send the same fft to the csd node to get PSD output
    scheme.add_edge(fft_index, csd_index, SchemeEdge::new(1));
    scheme.add_edge(fft_index, csd_index, SchemeEdge::new(2));

    scheme.add_edge(csd_index, real_index, SchemeEdge::new(1));
    scheme.add_edge(real_index, avg_index, SchemeEdge::new(1));
    scheme.add_edge(avg_index, sqrt_index, SchemeEdge::new(1));
    scheme.add_edge(sqrt_index, results_index, SchemeEdge::new(1).set_result_wrapper(EdgeResultsWrapper::ASD));
    
    // test the scheme graphs
    test_schemes(rc, &scheme, &SchemeGraph::new())?;
    
    // get the list of channels
    

    // Convert the scheme graph to a real analysis graph
    let channels: Vec<_> = view.set.clone().into();
    let chans: Vec<_> = channels.into_iter().map(|x|{x.into()}).collect();
    let graph = create_analysis_graph(chans.as_slice(), &scheme, &SchemeGraph::new())?;

    Ok(graph)
}

