"use strict";
(self["webpackChunk_dfnotebook_dfnotebook_extension"] = self["webpackChunk_dfnotebook_dfnotebook_extension"] || []).push([["dfgraph_lib_index_js"],{

/***/ "../dfgraph/lib/depview.js":
/*!*********************************!*\
  !*** ../dfgraph/lib/depview.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DepView: () => (/* binding */ DepView)
/* harmony export */ });
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! d3 */ "../../node_modules/d3/src/index.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jquery */ "../../node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _hpcc_js_wasm__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @hpcc-js/wasm */ "../../node_modules/@hpcc-js/wasm/dist/index.js");
/* harmony import */ var graphlib_dot__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! graphlib-dot */ "../../node_modules/graphlib-dot/index.js");
/* harmony import */ var graphlib_dot__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(graphlib_dot__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var d3_graphviz__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! d3-graphviz */ "../../node_modules/d3-graphviz/index.js");
/* harmony import */ var graphlib__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! graphlib */ "../../node_modules/graphlib/index.js");
/* harmony import */ var graphlib__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(graphlib__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @dfnotebook/dfutils */ "webpack/sharing/consume/default/@dfnotebook/dfutils/@dfnotebook/dfutils");
/* harmony import */ var _dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_6__);







//UUID length has been changed need to compensate for that
const uuidLength = 8;
const defaultOptions = {
    height: 1600,
    width: 1600,
    scale: 1,
    tweenPrecision: 1,
    engine: 'dot',
    keyMode: 'title',
    convertEqualSidedPolygons: false,
    fade: false,
    growEnteringEdges: false,
    fit: true,
    tweenPaths: false,
    tweenShapes: false,
    useWorker: false,
    zoom: true
};
class DepView {
    constructor(dfgraph, parentdiv, labelstyles) {
        //
        //         /** @method bind_events */
        //FIXME: Figure out Jupyter.notebook equivalent here
        //     bind_events = function () {
        //         var that = this;
        //         var nb = Jupyter.notebook;
        //
        //         nb.events.on('create.Cell', function(evt,cell) {
        //             if(that.is_open){
        //                 that.update_cell_lists();
        //             }
        //         });
        //         nb.events.on('select.Cell', function(){
        //             var cell = Jupyter.notebook.get_selected_cell();
        //            if(cell.cell_type === 'code' && that.is_open){
        //                that.set_details(cell.uuid);
        //            }
        //         });
        //         nb.events.on('delete.Cell',function (evt,cell) {
        //             if(that.is_open){
        //                 that.decorate_cell(cell.cell.uuid,'deleted-cell',true);
        //             }
        //         });
        //     };
        //
        /** @method closes the depviewer **/
        this.closeDiv = function () {
            this.isOpen = false;
            this.depdiv.style.display = 'none';
            d3__WEBPACK_IMPORTED_MODULE_0__.select(this.parentdiv).transition().delay(100).style('height', '0vh');
            d3__WEBPACK_IMPORTED_MODULE_0__.select('.end_space').transition().delay(100).style('height', '0vh');
        };
        this.updateOrder = function (order, active) {
            let old_order = this.order.slice();
            this.order = order;
            if (active && this.is_open && this.arraysEqual(old_order, this.order)) {
                this.startGraphCreation();
            }
        };
        //Taken from https://stackoverflow.com/questions/3115982/how-to-check-if-two-arrays-are-equal-with-javascript
        this.arraysEqual = function (a, b) {
            if (a === b)
                return true;
            if (a == null || b == null)
                return false;
            if (a.length !== b.length)
                return false;
            let bcopy = b.slice();
            a.sort();
            bcopy.sort();
            for (var i = 0; i < a.length; ++i) {
                if (a[i] !== bcopy[i])
                    return false;
            }
            return true;
        };
        //
        //     /** @method closes the depviewer and scrolls to the currently selected cell **/
        //     close_and_scroll = function () {
        //       var that = this;
        //       if(that.active_cell && that.active_cell !== ''){
        //           that.close_div();
        //           Jupyter.notebook.select_by_id(that.active_cell);
        //           Jupyter.notebook.scroll_to_cell_id(that.active_cell);
        //           return;
        //       }
        //       that.close_div();
        //     };
        //
        //
        this.setTracker = function (tracker) {
            this.tracker = tracker;
            console.log(tracker);
        };
        /** @method creates dependency div*/
        this.createDepDiv = function () {
            let that = this;
            this.depdiv = document.createElement('div');
            this.depdiv.setAttribute('class', 'dep-div container');
            jquery__WEBPACK_IMPORTED_MODULE_1___default()(this.parentdiv).append(this.depdiv);
            this.sidePanel = d3__WEBPACK_IMPORTED_MODULE_0__.select('div.dep-div')
                .append('div')
                .attr('id', 'side-panel');
            this.tabular = this.sidePanel
                .append('div')
                .attr('id', 'table')
                .classed('card', true);
            //        this.tabular.append('h3').text("Graph Overview").classed('card-header', true).classed('primary-color', true).classed('white-text', true).classed('cell-list-header', true).attr('id', 'overview-header');
            //         let newdiv = this.tabular.append('div').classed('table-div',true);
            //         newdiv.append('h4').text('New Cells').classed('card-header', true).classed('primary-color', true).classed('white-text', true).classed('cell-list-header', true);
            //         newdiv.append('div').classed('card-body', true).attr('id', 'newlist').append('ul').classed('list-group', true).classed('list-group-flush', true);
            //
            //         let changediv = this.tabular.append('div').classed('table-div',true);
            //         changediv.append('h4').text('Changed Cells').classed('card-header', true).classed('primary-color', true).classed('white-text', true).classed('cell-list-header', true);
            //         changediv.append('div').classed('card-body', true).attr('id', 'changedlist').append('ul').classed('list-group', true).classed('list-group-flush', true);
            this.tabular
                .append('a')
                .text('⤓ Dot')
                .attr('id', 'dot-dl')
                .classed('btnviz', true)
                .classed('btnviz-primary', true)
                .classed('fa', true); //.classed('btnviz', true).classed('btnviz-outline-primary', true).classed('btnviz-rounded waves-effect', true);
            this.tabular
                .append('a')
                .text('Toggle Sink Cells')
                .attr('id', 'out-toggle')
                .classed('btnviz', true)
                .classed('btnviz-primary', true)
                .classed('fa', true) //.classed('btnviz', true).classed('btnviz-outline-primary', true).classed('btnviz-rounded waves-effect', true)
                .on('click', function () {
                that.dataflow = !that.dataflow;
                that.startGraphCreation();
            });
            //FIXME: This is where the Graph Summary button goes
            //this.tabular.append('a').text('Show Graph Summary').attr('id', 'graphsum').classed('btnviz', true).classed('btnviz-outline-primary', true).classed('btnviz-rounded waves-effect', true);
            //        this.executepanel = this.side_panel.append('div').attr('id', 'cell-detail').classed('card', true).style('background-color', 'white');
            //        this.executepanel.append('h3').text("Cell Overview").classed('card-header', true).classed('primary-color', true).classed('white-text', true).classed('cell-list-header', true).attr('id', 'overview-header');
            this.tabular
                .append('span')
                .text('Cell Local Variables:')
                .classed('locals', true); //.classed('card-title', true);
            this.tabular
                .data(['None'])
                .append('span')
                .text('None')
                .classed('badge-pill', true)
                .classed('badge-danger', true);
            //         this.nodespanel = this.executepanel.append('div').attr('id', 'nodes-panel');
            //         this.nodespanel.append('h4').text("Cell Local Variables:").classed('card-title', true);
            //         this.nodespanel.data(["None"]).append('span').text('None').classed('badge-pill', true).classed('badge-danger', true);
            //let executeactions = this.executepanel.append('div').attr('id','exec-actions');
            //FIME:FIX THIS
            // executeactions.append('a').text("  Execute Cell").classed('btnviz', true).classed('btnviz-primary', true).attr('id', 'exec-button').classed('fa-step-forward', true).classed('fa', true).on('click',function(){
            //     var cell = Jupyter.notebook.get_selected_cell();
            //     cell.execute();
            // });
            //executeactions.append('a').text("Close and Go to Cell").attr('id', 'close-scroll').classed('btnviz', true).classed('btnviz-primary', true).classed('fa', true).on('click', function () {that.close_and_scroll();});
            this.svg = d3__WEBPACK_IMPORTED_MODULE_0__.select('div.dep-div')
                .append('div')
                .attr('id', 'svg-div')
                .on('contextmenu', function () {
                return false;
            });
            this.isCreated = true;
        };
        /** @method upon a new cell selection will change the details of the viewer **/
        this.setDetails = function (cellid) {
            let that = this;
            jquery__WEBPACK_IMPORTED_MODULE_1___default()('#' + that.activeCell + 'cluster')
                .find('polygon')
                .toggleClass('selected', false);
            that.activeCell = cellid;
            d3__WEBPACK_IMPORTED_MODULE_0__.select('#select-identifier').remove();
            if (that.dfgraph.getCells().indexOf(that.activeCell) > -1) {
                // @ts-ignore
                let rectPoints = jquery__WEBPACK_IMPORTED_MODULE_1___default()('#' + that.activeCell + 'cluster')
                    .find('polygon')
                    .attr('points')
                    .split(' ');
                let rectTop = rectPoints[1].split(',');
                let height = Math.abs(rectTop[1] - Number(rectPoints[0].split(',')[1]));
                d3__WEBPACK_IMPORTED_MODULE_0__.select('#svg-div svg g')
                    .insert('g', '#a_graph0 + *')
                    .attr('id', 'select-identifier')
                    .append('rect')
                    .attr('x', parseInt(rectTop[0]) - 3)
                    .attr('y', parseInt(rectTop[1]))
                    .attr('height', height)
                    .attr('width', '3px');
            }
            //FIXME: Find equivalent in Lab
            //console.log(NotebookTools);
            //const cell = panel.content.widgets[index];
            //cell.node.scrollIntoView();
            //Jupyter.notebook.select_by_id(that.active_cell);
            //Jupyter.notebook.scroll_to_cell_id(that.active_cell);
            this.tracker.currentWidget.content.activeCellIndex =
                this.order.indexOf(cellid);
            jquery__WEBPACK_IMPORTED_MODULE_1___default()('#' + cellid + 'cluster')
                .find('polygon')
                .toggleClass('selected', true);
            d3__WEBPACK_IMPORTED_MODULE_0__.select('#table').selectAll('.badge-pill').remove();
            let intNodes = that.dfgraph.getInternalNodes(cellid);
            if (intNodes.length < 1) {
                intNodes = ['None'];
            }
            d3__WEBPACK_IMPORTED_MODULE_0__.select('#table')
                .selectAll('span.badge')
                .data(intNodes)
                .enter()
                .append('span')
                .text(function (d) {
                return d;
            })
                .attr('class', function (d) {
                let baseclasses = 'badge badge-pill ';
                if (d === 'None') {
                    return baseclasses + 'badge-danger';
                }
                return baseclasses + 'badge-primary';
            });
        };
        /** @method updates the new and changed cell lists **/
        this.updateCellLists = function () {
            let that = this;
            //let new_cells: string[] = [];
            //let changed_cells: string[] = [];
            //Goes with code below
            //var cells = that.dfgraph.get_cells();
            //FIXME: Find Jupyter Equivalent
            // Jupyter.notebook.get_cells().map(function(cell){
            //     if(cell.cell_type === 'code'){
            //         if(cells.indexOf(cell.uuid) > -1){
            //             if(cell.metadata.cell_status.substr(0,'edited'.length) === 'edited'){
            //                 changed_cells.push(cell.uuid);
            //             }
            //         }
            //         else{
            //             new_cells.push(cell.uuid);
            //         }
            //     }
            // });
            // TODO: REMOVE THIS FUNCTIONALITY, REVISIT AT SOME POINT?
            //             let new_list = d3.select('#newlist').select('ul').selectAll('li').data(new_cells);
            //
            //             new_list.attr('id',function(d){return 'viz-'+d;}).classed('cellid',true)
            //             .html(function(d){return 'In['+d+']';}).enter()
            //             .append('li').classed('list-group-item',true).append('a').classed('cellid',true).attr('id',function(d){return 'viz-'+d;})
            //             .html(function(d){return 'In['+d+']';});
            //
            //             new_list.exit().attr('opacity',1).transition().delay(500).attr('opacity',0).remove();
            //
            //             let changed_list = d3.select('#changedlist').select('ul').selectAll('li').data(changed_cells);
            //
            //             changed_list.attr('id',function(d){return 'viz-'+d;}).classed('cellid',true)
            //             .html(function(d){return 'In['+d+']';}).enter()
            //             .append('li').classed('list-group-item',true).append('a').classed('cellid',true).attr('id',function(d){return 'viz-'+d;})
            //             .html(function(d){return 'In['+d+']';});
            //
            //             changed_list.exit().attr('opacity',1).transition().delay(500).attr('opacity',0).remove();
            d3__WEBPACK_IMPORTED_MODULE_0__.select('#table')
                .selectAll('.cellid')
                .on('click', function (d) {
                that.setDetails(d);
            });
            //that.decorate_cells(changed_cells,'changed-cell',true);
        };
        this.decorateCells = function (cells, cssClass, allCells) {
            cells = cells || [];
            allCells = allCells || false;
            if (allCells) {
                jquery__WEBPACK_IMPORTED_MODULE_1___default()('.cluster').find('polygon').toggleClass(cssClass, false);
            }
            cells.forEach(function (uuid) {
                jquery__WEBPACK_IMPORTED_MODULE_1___default()('#' + uuid + 'cluster')
                    .find('polygon')
                    .toggleClass(cssClass, true);
            });
        };
        this.decorateCell = function (uuid, cssClass, toggle) {
            if (this.isOpen) {
                uuid = uuid || '';
                jquery__WEBPACK_IMPORTED_MODULE_1___default()('#' + uuid + 'cluster')
                    .find('polygon')
                    .toggleClass(cssClass, toggle);
            }
        };
        /** @method this creates and renders the actual visual graph **/
        this.createGraph = function (g) {
            let that = this;
            g.nodes().forEach(function (v) {
                let node = g.node(v);
                // Round the corners of the nodes
                node.rx = node.ry = 5;
            });
            that.dotgraph = graphlib_dot__WEBPACK_IMPORTED_MODULE_3___default().write(g);
            //FIXME: Something weird is going on here with the transitions if you declare them at the start they fail
            //but if you declare them here there is a large delay before the transition happens
            that.graphtran = d3__WEBPACK_IMPORTED_MODULE_0__.transition().duration(750).ease(d3__WEBPACK_IMPORTED_MODULE_0__.easeLinear);
            //FIXME: Not ideal way to be set this up, graphviz requires a set number of pixels for width and height
            (0,d3_graphviz__WEBPACK_IMPORTED_MODULE_4__.graphviz)('#svg-div')
                .options(defaultOptions)
                .on('end', function () {
                that.updateCellLists();
                that.doneRendering = true;
            })
                .transition(that.graphtran)
                .renderDot(that.dotgraph);
            let dotURL = URL.createObjectURL(new Blob([that.dotgraph], { type: 'text/plain;charset=utf-8' }));
            jquery__WEBPACK_IMPORTED_MODULE_1___default()('#dot-dl').attr('href', dotURL).attr('download', 'graph.dot');
            jquery__WEBPACK_IMPORTED_MODULE_1___default()('g.parentnode.cluster').each(function () {
                jquery__WEBPACK_IMPORTED_MODULE_1___default()(this)
                    .mouseover(function () {
                    let node = jquery__WEBPACK_IMPORTED_MODULE_1___default()(this), cellid = node
                        .find('text')
                        .text()
                        .substr(that.cellLabel.length, uuidLength);
                    that.setDetails(cellid);
                    //var cell = Jupyter.notebook.get_code_cell(cellid);
                    that.dfgraph.getDownstreams(cellid).forEach(function (t) {
                        jquery__WEBPACK_IMPORTED_MODULE_1___default()('#' + t.substr(0, uuidLength) + 'cluster')
                            .find('polygon')
                            .toggleClass('upcell', true);
                        jquery__WEBPACK_IMPORTED_MODULE_1___default()('g.' + cellid + t.substr(0, uuidLength))
                            .find('path')
                            .toggleClass('upstream', true);
                    });
                    that.dfgraph.getImmUpstreams(cellid).forEach(function (t) {
                        jquery__WEBPACK_IMPORTED_MODULE_1___default()('#' + t.substr(0, uuidLength) + 'cluster')
                            .find('polygon')
                            .toggleClass('downcell', true);
                        jquery__WEBPACK_IMPORTED_MODULE_1___default()('g.' + t.substr(0, uuidLength) + cellid)
                            .find('path')
                            .toggleClass('downstream', true);
                    });
                })
                    .on('mouseout', function () {
                    //var node = $(this);
                    //cellid = node.find('text').text().substr(that.cell_label.length,uuid_length);
                    //var cell = Jupyter.notebook.get_code_cell(cellid);
                    jquery__WEBPACK_IMPORTED_MODULE_1___default()('.edge').each(function () {
                        jquery__WEBPACK_IMPORTED_MODULE_1___default()(this)
                            .find('path')
                            .toggleClass('upstream', false)
                            .toggleClass('downstream', false);
                    });
                    jquery__WEBPACK_IMPORTED_MODULE_1___default()('g.parentnode, .cluster')
                        .each(function () {
                        jquery__WEBPACK_IMPORTED_MODULE_1___default()(this)
                            .find('polygon')
                            .toggleClass('upcell', false)
                            .toggleClass('downcell', false);
                    })
                        .contextmenu(function () {
                        return false;
                    });
                });
            });
            jquery__WEBPACK_IMPORTED_MODULE_1___default()('g.child-node').each(function () {
                jquery__WEBPACK_IMPORTED_MODULE_1___default()(this)
                    .mouseover(function () {
                    jquery__WEBPACK_IMPORTED_MODULE_1___default()('.viz-' + jquery__WEBPACK_IMPORTED_MODULE_1___default()(this).find('title').text()).each(function () {
                        jquery__WEBPACK_IMPORTED_MODULE_1___default()(this).find('path').toggleClass('upstream', true);
                        jquery__WEBPACK_IMPORTED_MODULE_1___default()(this).find('polygon').toggleClass('upcell', true);
                    });
                })
                    .mouseout(function () {
                    jquery__WEBPACK_IMPORTED_MODULE_1___default()('.viz-' + jquery__WEBPACK_IMPORTED_MODULE_1___default()(this).find('title').text()).each(function () {
                        jquery__WEBPACK_IMPORTED_MODULE_1___default()(this).find('path').toggleClass('upstream', false);
                    });
                    jquery__WEBPACK_IMPORTED_MODULE_1___default()(this).find('polygon').toggleClass('upcell', false);
                });
            });
            //FIXME: Fix the Jupyter notebook reference here
            //var deleted_cells = Object.keys(Jupyter.notebook.metadata.hl_list || []);
            //that.decorate_cells(deleted_cells,'deleted-cell',true);
            jquery__WEBPACK_IMPORTED_MODULE_1___default()('g.parentnode.cluster').on('mousedown', function (event) {
                if (event.which == 1) {
                    that.closeAndScroll();
                }
            });
            //FIXME: Fix this
            // .on("contextmenu",function(event){
            //     var cellid = $(this).find('text').text().substr(that.cell_label.length, uuid_length);
            //     Jupyter.notebook.get_code_cell(cellid).execute();
            // });
        };
        /** @method this ellides the names of output nodes **/
        this.getNodes = function (uuid) {
            return this.dfgraph.getNodes(uuid).map(function (a) {
                return a.length > 10 ? a.substring(0, 7) + '..' : a;
            });
        };
        /** @method this creates the graphlib data structure that is used to create the visualization **/
        this.createNodeRelations = function () {
            let that = this;
            that.cellLinks = [];
            that.cellList = [];
            that.cellChildNums = [];
            that.outputNodes = [];
            let outnames = [];
            if (that.dataflow) {
                //Should provide a better experience since order handles deletions
                that.updateOrder(that.tracker.currentWidget.model.cells.model.cells.map((cell) => cell.id), false);
                that.cellList = that.order.map((cell) => (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_6__.truncateCellId)(cell));
                that.cellList.forEach(function (uuid) {
                    that.outputNodes[uuid] = that.getNodes(uuid);
                    outnames = that.outputNodes[uuid];
                    that.dfgraph.getUpstreams(uuid).forEach(function (b) {
                        b = b.length > 10 ? b.substring(0, 7) + '..' : b;
                        if (outnames.indexOf(uuid) > -1) {
                            that.cellLinks.push({ source: b, target: uuid });
                        }
                        else {
                            that.cellLinks.push({ source: b, target: uuid + '-Cell' });
                        }
                    });
                });
                //FIXME: Change this
                that.cellList = that.cellList.map(function (uuid) {
                    return { id: uuid };
                });
            }
            else {
                //Should provide a better experience
                that.updateOrder(that.tracker.currentWidget.model.cells.model.cells.map((cell) => cell.id), false);
                that.cellList = that.order.map((cell) => (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_6__.truncateCellId)(cell));
                that.cellList.forEach(function (uuid) {
                    that.outputNodes[uuid] = that.getNodes(uuid);
                    if (that.outputNodes[uuid].length == 0) {
                        delete that.outputNodes[uuid];
                        return;
                    }
                    outnames = that.outputNodes[uuid];
                    if (uuid in that.outputNodes && that.cellList.indexOf(uuid) > 1) {
                        that.dfgraph.getUpstreams(uuid).forEach(function (b) {
                            b = b.length > 10 ? b.substring(0, 7) + '..' : b;
                            if (outnames.indexOf(uuid) > -1) {
                                that.cellLinks.push({ source: b, target: uuid });
                            }
                            else {
                                outnames.forEach(function (t) {
                                    that.cellLinks.push({ source: b, target: uuid + t });
                                });
                            }
                        });
                    }
                });
                //FIXME: Change this
                that.cellList = Object.keys(that.outputNodes).map(function (t) {
                    return { id: t };
                });
            }
            that.cellList.forEach(function (a) {
                that.cellChildNums[a.id] = 0;
            });
            that.cellLinks.forEach(function (a) {
                that.cellChildNums[a.source] += 1;
            });
            let g = new graphlib__WEBPACK_IMPORTED_MODULE_5__.Graph({ compound: true })
                .setGraph({
                compound: true,
                ranksep: 1,
                nodesep: 0.03,
                tooltip: ' ',
                rankdir: 'LR'
            })
                .setDefaultEdgeLabel(function () {
                return {};
            });
            that.cellList.forEach(function (a) {
                if (that.outputNodes[a.id]) {
                    if (that.selected && a.level == 0) {
                        g.setNode('cluster_Out[' + a.id + ']', {
                            label: that.cellLabel + a.id,
                            id: 'selected',
                            clusterLabelPos: 'top',
                            class: 'parentnode cellid',
                            shape: 'box',
                            margin: 5
                        });
                    }
                    else {
                        g.setNode('cluster_Out[' + a.id + ']', {
                            label: that.cellLabel + a.id,
                            id: a.id + 'cluster',
                            clusterLabelPos: 'top',
                            class: 'parentnode cellid',
                            tooltip: ' ',
                            shape: 'box',
                            margin: 5
                        });
                    }
                }
            });
            Object.keys(that.outputNodes).forEach(function (a) {
                let parent = 'cluster_Out[' + a + ']';
                if (that.dataflow || that.selected) {
                    let cell = a + '-Cell';
                    g.setNode(cell, {
                        label: 'Cell[' + a + ']',
                        class: 'child-node prompt output_prompt cellid',
                        labelStyle: that.labelstyles,
                        style: 'invis',
                        peripheries: 0,
                        height: 0,
                        width: 0,
                        margin: '0,0',
                        tooltip: ' ',
                        shape: 'point',
                        id: cell
                    });
                    g.setParent(cell, parent);
                }
                that.outputNodes[a].forEach(function (t) {
                    //var uuid = t.substr(4,uuid_length);
                    //FIXME: Make this more robust so it uses uuid_length
                    if (/cluster_Out\_[a-f0-9]{8}/.test(t)) {
                        g.setNode(a + t, {
                            label: parent,
                            class: 'child-node prompt output_prompt cellid',
                            labelStyle: that.labelstyles,
                            tooltip: ' ',
                            shape: 'box',
                            id: a + t,
                            width: 0.2,
                            height: 0.05,
                            margin: '0.1,0.01'
                        });
                        g.setParent(a + t, parent);
                    }
                    else {
                        g.setNode(a + t, {
                            label: t,
                            class: 'child-node prompt output_prompt cellid',
                            labelStyle: that.labelstyles,
                            tooltip: ' ',
                            shape: 'box',
                            id: a + t,
                            width: 0.2,
                            height: 0.05,
                            margin: '0.1,0.01'
                        });
                        g.setParent(a + t, parent);
                    }
                });
            });
            that.cellLinks.forEach(function (a) {
                if (g.hasNode(a.source) && g.hasNode(a.target)) {
                    g.setEdge(a.source, a.target, {
                        class: a.source.substr(0, uuidLength) +
                            a.target.substr(0, uuidLength) +
                            ' viz-' +
                            a.source,
                        id: 'viz-' + a.source + a.target,
                        lhead: 'cluster_Out[' + a.target.substr(0, uuidLength) + ']'
                    });
                }
            });
            if (that.debugMode) {
                console.log(that.cellList);
                console.log(that.outputNodes);
                console.log(that.cellLinks);
                console.log(g.children());
                console.log(g.nodes());
                console.log(g.edges());
                console.log(graphlib_dot__WEBPACK_IMPORTED_MODULE_3___default().write(g));
            }
            return g;
        };
        /** @method this opens and closes the depviewer **/
        this.toggleDepView = function () {
            let that = this;
            if (this.isOpen) {
                that.closeDiv();
            }
            else {
                that.isOpen = true;
                //that.active_cell = Jupyter.notebook.get_selected_cell().uuid;
                //FIXME: Doesn't currently exist in this version
                //var deleted_cells = Object.keys(Jupyter.notebook.metadata.hl_list || []);
                //that.decorate_cells(deleted_cells,'deleted-cell',true);
                //FIXME: Possibly change this?
                //GraphViz relies on the size of the svg to make the initial adjustments so the svg has to be sized first
                d3__WEBPACK_IMPORTED_MODULE_0__.select(that.parentdiv)
                    .transition()
                    .delay(100)
                    .style('height', '60vh')
                    .on('end', function () {
                    if (that.dfgraph.wasChanged) {
                        that.doneRendering = false;
                        that.startGraphCreation();
                    }
                });
                d3__WEBPACK_IMPORTED_MODULE_0__.select('.end_space').transition().delay(100).style('height', '60vh');
                that.depdiv.style.display = 'block';
            }
        };
        /** @method starts graph creation **/
        this.startGraphCreation = function () {
            let that = this;
            let g = this.createNodeRelations();
            this.createGraph(g);
            that.dfgraph.wasChanged = false;
        };
        /** @method set graph, sets the current activate graph to be visualized */
        this.setGraph = function (graph) {
            this.dfgraph = graph;
        };
        //Flags
        this.isOpen = false;
        this.dataflow = true;
        this.selected = false;
        this.doneRendering = false;
        this.isCreated = false;
        //Turn on console logs
        this.debugMode = false;
        //Divs and Div related variables
        this.parentdiv = parentdiv || 'div#depview';
        this.depdiv = null;
        this.sidePanel = null;
        this.nodespanel = null;
        this.svg = null;
        this.tabular = null;
        this.executePanel = null;
        //Label Styles should be set in text so that GraphViz can properly size the nodes
        this.labelstyles =
            labelstyles ||
                'font-family: monospace; fill: #D84315; font-size: 0.85em;';
        //Divs are created and defined in here
        //this.createDepDiv();
        //This has been largely factored out but this provides the option to change the label of a cell
        this.cellLabel = '';
        this.cellLinks = [];
        this.order = [];
        this.cellList = [];
        this.cellChildNums = [];
        this.outputNodes = [];
        this.activeCell = '';
        this.dfgraph = dfgraph;
        this.graphtran = null;
        //console.log(NotebookTools);
        this.dotgraph = [];
        //this.bind_events();
    }
}


/***/ }),

/***/ "../dfgraph/lib/dfgraph.js":
/*!*********************************!*\
  !*** ../dfgraph/lib/dfgraph.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Graph: () => (/* binding */ Graph),
/* harmony export */   Manager: () => (/* binding */ Manager)
/* harmony export */ });
/* harmony import */ var _dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @dfnotebook/dfutils */ "webpack/sharing/consume/default/@dfnotebook/dfutils/@dfnotebook/dfutils");
/* harmony import */ var _dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _depview__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./depview */ "../dfgraph/lib/depview.js");
/* harmony import */ var _minimap__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./minimap */ "../dfgraph/lib/minimap.js");



//UUID length has been changed need to compensate for that
const uuidLength = 8;
/** @method this is a set addition method for dependencies */
// @ts-ignore
Array.prototype.setAdd = function (item) {
    let that = this;
    if (that.indexOf(item) < 0) {
        that.push(item);
    }
};
class GraphManager {
    constructor(graphs) {
        this.getProperty = function (prop) {
            if (prop in this.graphs) {
                // @ts-ignore
                return this.graphs[prop];
            }
            return '';
        };
        this.setTracker = function (tracker) {
            this.tracker = tracker;
            this.minimap.setTracker(this.tracker);
            this.depview.setTracker(this.tracker);
        };
        /** @method updates the activate graph and calls the update views method */
        this.updateGraph = function (graph) {
            if (graph == 'None') {
                return;
            }
            this.currentGraph = graph;
            this.depview.dfgraph = this.graphs[graph];
            this.minimap.setGraph(this.graphs[graph]);
            this.updateDepViews(true);
        };
        this.updateActive = function (activeid, prevActive) {
            this.activeID = activeid || 'none';
            this.previousActive = prevActive || 'none';
            //FIXME: Add depviewer active cell code
            //         if(this.depWidget.is_open){
            //             console.log("Update dep viewer here");
            //         }
            if (this.miniWidget && this.miniWidget.isOpen) {
                this.minimap.updateActiveByID(activeid);
            }
        };
        /** @method attempt to update the active graph using the tracker this is not preferred **/
        this.updateActiveGraph = function () {
            var _a;
            this.currentGraph =
                ((_a = this.tracker.currentWidget.sessionContext.session) === null || _a === void 0 ? void 0 : _a.id) || 'None';
            this.depview.dfgraph = this.graphs[this.currentGraph];
            this.minimap.setGraph(this.graphs[this.currentGraph]);
            this.updateDepViews(true, false, true);
        };
        this.markStale = function (uuid) {
            this.updateActiveGraph();
            if (!(this.currentGraph in this.graphs)) {
                return;
            }
            this.graphs[this.currentGraph].updateStale(uuid);
            if (this.miniWidget.isOpen) {
                this.minimap.updateStates();
            }
        };
        this.revertStale = function (uuid) {
            this.graphs[this.currentGraph].updateFresh(uuid, true);
            if (this.miniWidget.isOpen) {
                this.minimap.updateStates();
            }
        };
        this.getStale = function (uuid) {
            return this.graphs[this.currentGraph].states[uuid];
        };
        this.getActive = function () {
            return this.previousActive;
        };
        this.getText = function (uuid) {
            this.updateActiveGraph();
            if (!(this.currentGraph in this.graphs)) {
                return '';
            }
            return this.graphs[this.currentGraph].cellContents[uuid];
        };
        this.updateOrder = function (neworder) {
            this.updateActiveGraph();
            if (!(this.currentGraph in this.graphs)) {
                return;
            }
            this.graphs[this.currentGraph].updateOrder(neworder);
            let modifiedorder = neworder.map((cellid) => (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_0__.truncateCellId)(cellid));
            this.minimap.updateOrder(modifiedorder);
            this.depview.updateOrder(modifiedorder, true);
            this.updateDepViews(true, true);
        };
        // Utility function to create an empty graph in case one doesn't exist
        this.createGraph = function (sess) {
            this.graphs[sess] = new Graph();
        };
        /** @method updates all viewers based on if they're open or not */
        // view flag is based on if it's a new view or the same view
        this.updateDepViews = function (newView, mini = false, mini2 = false) {
            if (this.miniWidget && this.miniWidget.isOpen) {
                if (mini2) {
                    return;
                }
                if (newView) {
                    this.minimap.clearMinimap();
                }
                this.minimap.startMinimapCreation();
            }
            if (this.depwidget && this.depWidget.isOpen && !mini) {
                if (newView) {
                    this.depview.startGraphCreation();
                }
                else {
                    let g = this.depview.createNodeRelations(this.depview.globaldf, this.depview.globalselect);
                    this.depview.createGraph(g);
                }
            }
        };
        this.graphs = graphs || {};
        this.currentGraph = 'None';
        this.depview = new _depview__WEBPACK_IMPORTED_MODULE_1__.DepView();
        this.minimap = new _minimap__WEBPACK_IMPORTED_MODULE_2__.Minimap();
        this.previousActive = 'None';
    }
}
class Graph {
    /*
     * Create a graph to contain all inner cell dependencies
     */
    constructor({ cells = [], nodes = [], uplinks = {}, downlinks = {}, internalNodes = {}, allDown = {}, cellContents = {} } = {}, states) {
        /** @method getText **/
        this.getText = function (uuid) {
            if (uuid in this.cellContents) {
                return this.cellContents[uuid];
            }
            return '';
        };
        this.updateOrder = function (neworder) {
            console.log(neworder);
            this.cellOrder = neworder;
        };
        /** @method removes a cell entirely from the graph **/
        this.removeCell = function (uuid) {
            let that = this;
            let cellIndex = that.cells.indexOf(uuid);
            if (cellIndex > -1) {
                that.cells.splice(cellIndex, 1);
                delete that.nodes[uuid];
                delete that.internalNodes[uuid];
                delete that.downstreamLists[uuid];
                (that.downlinks[uuid] || []).forEach(function (down) {
                    if (down in that.uplinks && uuid in that.uplinks[down]) {
                        delete that.uplinks[down][uuid];
                    }
                });
                delete that.downlinks[uuid];
                if (uuid in that.uplinks) {
                    let uplinks = Object.keys(that.uplinks[uuid]);
                    uplinks.forEach(function (up) {
                        let idx = that.downlinks[up].indexOf(uuid);
                        that.downlinks[up].splice(idx, 1);
                    });
                }
                delete that.uplinks[uuid];
                if (uuid in that.upstreamList) {
                    // @ts-ignore
                    let allUps = that.upstreamList[uuid].slice(0);
                    // @ts-ignore
                    delete that.upstreamList[uuid];
                    allUps.forEach(function (up) {
                        //Better to just invalidate the cached list so you don't have to worry about downstreams too
                        delete that.downstreamLists[up];
                    });
                }
            }
        };
        /** @method setInternalNodes */
        this.setInternalNodes = function (uuid, internalNodes) {
            this.internalNodes[uuid] = internalNodes;
        };
        /** @method returns all cells on kernel side*/
        this.getCells = function () {
            return this.cells;
        };
        let that = this;
        this.wasChanged = false;
        this.cells = cells || [];
        this.nodes = nodes || [];
        this.uplinks = uplinks || {};
        this.downlinks = downlinks || {};
        this.internalNodes = internalNodes || {};
        this.cellContents = cellContents || {};
        this.cellOrder = [];
        //Cache downstream lists
        this.downstreamLists = allDown || {};
        this.upstreamList = {};
        this.states = states || {};
        this.executed = {};
        if (that.cells.length > 1) {
            that.cells.forEach(function (uuid) {
                that.states[uuid] = 'Stale';
                that.executed[uuid] = false;
            });
        }
    }
    /** @method updateStale updates the stale states in the graph */
    updateStale(uuid) {
        this.states[uuid] = 'Changed';
        if (uuid in this.downlinks) {
            this.allDownstream(uuid).forEach((duuid) => (this.states[duuid] = 'Upstream Stale'));
        }
    }
    /** @method updateFresh updates the stale states in the graph */
    updateFresh(uuid, revert) {
        let that = this;
        //Make sure that we don't mark non executed cells as fresh
        if (revert && !that.executed[uuid]) {
            return;
        }
        that.states[uuid] = 'Fresh';
        that.executed[uuid] = true;
        //We have to execute upstreams either way
        console.log(that.uplinks[uuid]);
        if (that.uplinks[uuid]) {
            Object.keys(that.uplinks[uuid]).forEach(function (upuuid) {
                that.states[upuuid] = 'Fresh';
            });
        }
        if (revert == true) {
            //Restore downstream statuses
            that.allDownstream(uuid).forEach(function (duuid) {
                if (that.upstreamFresh(duuid) &&
                    that.states[duuid] == 'Upstream Stale') {
                    that.states[duuid] = 'Fresh';
                }
            });
        }
    }
    /** @method upstreamFresh checks to see if everything upstream from a cell is fresh or not */
    upstreamFresh(uuid) {
        let that = this;
        return Object.keys(that.getAllUpstreams(uuid)).reduce(function (flag, upuuid) {
            return flag && that.states[upuuid] == 'Fresh';
        }, true);
    }
    /** @method updateGraph */
    updateGraph(cells, nodes, uplinks, downlinks, uuid, allUps, internalNodes) {
        let that = this;
        //         if(that.depview.isOpen === false){
        //             that.wasChanged = true;
        //         }
        that.cells = cells;
        that.nodes[uuid] = nodes || [];
        if (uuid in that.uplinks && that.uplinks[uuid]) {
            Object.keys(that.uplinks[uuid]).forEach(function (uplink) {
                that.downlinks[uplink] = [];
            });
        }
        that.uplinks[uuid] = uplinks;
        that.downlinks[uuid] = downlinks || [];
        that.internalNodes[uuid] = internalNodes;
        that.updateDepLists(allUps, uuid);
        that.updateFresh(uuid, false);
        //Shouldn't need the old way of referencing
        //that.minimap.updateEdges();
        //celltoolbar.CellToolbar.rebuildAll();
    }
    /** @method recursively yield all downstream deps */
    allDownstream(uuid) {
        let that = this;
        let visited = []; // Array<string> = [];
        let res = []; //: Array<string> = [];
        let downlinks = (this.downlinks[uuid] || []).slice(0);
        while (downlinks.length > 0) {
            let cid = downlinks.pop();
            visited.setAdd(cid);
            res.setAdd(cid);
            if (cid in that.downstreamLists) {
                that.downstreamLists[cid].forEach(function (pid) {
                    res.setAdd(pid);
                    visited.setAdd(pid);
                });
            }
            else {
                if (cid in that.downlinks) {
                    that.downlinks[cid].forEach(function (pid) {
                        if (visited.indexOf(pid) < 0) {
                            downlinks.push(pid);
                        }
                    });
                }
                else {
                    let idx = res.indexOf(cid);
                    res.splice(idx, 1);
                }
            }
        }
        that.downstreamLists[uuid] = res;
        return res;
    }
    allUpstreamCellIds(cid) {
        let uplinks = this.getImmUpstreams(cid);
        let allCids = [];
        while (uplinks.length > 0) {
            let upCid = uplinks.pop() || '';
            allCids.setAdd(upCid);
            uplinks = uplinks.concat(this.getImmUpstreams(upCid));
        }
        return allCids;
    }
    /** @method updates all downstream links with downstream updates passed from kernel */
    updateDownLinks(downupdates) {
        let that = this;
        downupdates.forEach(function (t) {
            let uuid = t['key'].substr(0, uuidLength);
            that.downlinks[uuid] = t['data'];
            if (uuid in that.cellContents && t.data) {
                that.downlinks[uuid] = t['data'];
            }
        });
        that.downstreamLists = {};
    }
    /** @method updateCodeDict */
    updateCellContents(cellContents) {
        this.cellContents = cellContents;
    }
    /** @method updateDepLists */
    updateDepLists(allUps, uuid) {
        let that = this;
        //     let cell = Jupyter.notebook.getCodeCell(uuid);
        //
        //     if(cell.last_msg_id){
        //         cell.clear_df_info();
        //     }
        //
        //     if(that.downlinks[uuid].length > 0){
        //         cell.updateDfList(cell,that.allDownstream(uuid),'downstream');
        //     }
        //
        if (allUps == undefined) {
            return;
        }
        if (allUps.length > 0) {
            // @ts-ignore
            that.upstreamList[uuid] = allUps;
            //        cell.updateDfList(cell,allUps,'upstream');
        }
    }
    /** @method returns the cached all upstreams for a cell with a given uuid */
    getAllUpstreams(uuid) {
        // @ts-ignore
        return this.upstreamList[uuid];
    }
    /** @method returns upstreams for a cell with a given uuid */
    getUpstreams(uuid) {
        let that = this;
        return Object.keys(that.uplinks[uuid] || []).reduce(function (arr, uplink) {
            let links = that.uplinks[uuid][uplink].map(function (item) {
                return uplink === item ? item : uplink + item;
            }) || [];
            return arr.concat(links);
        }, []);
    }
    /** @method returns single cell based upstreams for a cell with a given uuid */
    getImmUpstreams(uuid) {
        // @ts-ignore
        if (uuid in this.uplinks) {
            // @ts-ignore
            return Object.keys(this.uplinks[uuid]);
        }
        return [];
    }
    getImmUpstreamNames(uuid) {
        let arr = [];
        let that = this;
        // @ts-ignore
        this.getImmUpstreams(uuid).forEach(function (upUuid) {
            // @ts-ignore
            Array.prototype.push.apply(arr, that.uplinks[uuid][upUuid]);
        });
        return arr;
    }
    getImmUpstreamPairs(uuid) {
        let arr = [];
        let that = this;
        if (uuid !== undefined) {
            this.getImmUpstreams(uuid.toString()).forEach(function (upUuid) {
                Array.prototype.push.apply(arr, that.uplinks[uuid][upUuid].map(function (v) {
                    return [v, upUuid];
                }));
            });
        }
        return arr;
    }
    /** @method returns downstreams for a cell with a given uuid */
    getDownstreams(uuid) {
        return this.downlinks[uuid];
    }
    /** @method returns the cached all upstreams for a cell with a given uuid */
    getInternalNodes(uuid) {
        return this.internalNodes[uuid] || [];
    }
    /** @method returns all nodes for a cell*/
    getNodes(uuid) {
        let that = this;
        if (uuid in that.nodes) {
            if ((that.nodes[uuid] || []).length > 0) {
                return that.nodes[uuid];
            }
        }
        return [];
    }
}
const Manager = new GraphManager();


/***/ }),

/***/ "../dfgraph/lib/index.js":
/*!*******************************!*\
  !*** ../dfgraph/lib/index.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Graph: () => (/* reexport safe */ _dfgraph__WEBPACK_IMPORTED_MODULE_0__.Graph),
/* harmony export */   Manager: () => (/* reexport safe */ _dfgraph__WEBPACK_IMPORTED_MODULE_0__.Manager),
/* harmony export */   ViewerWidget: () => (/* reexport safe */ _viewer__WEBPACK_IMPORTED_MODULE_1__.ViewerWidget)
/* harmony export */ });
/* harmony import */ var _dfgraph__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./dfgraph */ "../dfgraph/lib/dfgraph.js");
/* harmony import */ var _viewer__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./viewer */ "../dfgraph/lib/viewer.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module dfgraph
 */




/***/ }),

/***/ "../dfgraph/lib/minimap.js":
/*!*********************************!*\
  !*** ../dfgraph/lib/minimap.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Minimap: () => (/* binding */ Minimap)
/* harmony export */ });
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! d3 */ "../../node_modules/d3/src/index.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jquery */ "../../node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @dfnotebook/dfutils */ "webpack/sharing/consume/default/@dfnotebook/dfutils/@dfnotebook/dfutils");
/* harmony import */ var _dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_2__);
//UUID length has been changed need to compensate for that
//FIXME: Future Include?
const uuidLength = 8;



class Minimap {
    constructor(dfgraph, parentdiv) {
        this.setTracker = function (tracker) {
            this.tracker = tracker;
        };
        /** @method update the order that cells are present in the minimap **/
        this.updateOrder = function (order) {
            //Have to set uuids properly here in case we rely on cell array
            this.order = order.map((uuid) => (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_2__.truncateCellId)(uuid));
            return true;
        };
        /** @method resets all paths **/
        this.reset = function () {
            this.svg.selectAll('.active').classed('active', false);
            this.svg.selectAll('.imm').classed('imm', false);
            this.svg.selectAll('.active_node').classed('active_node', false);
            this.svg.selectAll('.move_left').classed('move_left', false);
            this.svg.selectAll('.move_right').classed('move_right', false);
            this.svg.selectAll('.hidden').classed('hidden', false);
            this.svg.selectAll('.gray').classed('gray', false);
            this.svg.selectAll('.joining').remove();
            this.svg.selectAll('.activeedge').remove();
        };
        /** @method creates paths between node segments **/
        this.makePaths = function (sourceCy, destinationCy, parent, left) {
            let xVal = left
                ? this.svgOffsetX + this.radius + this.pathOffset
                : this.svgOffsetX - (this.radius + this.pathOffset);
            let yVal = destinationCy - sourceCy;
            parent
                .append('path')
                .classed('joining', true)
                .attr('d', 'M' + xVal + ' ' + sourceCy + 'v ' + yVal)
                .attr('stroke-width', this.strokeWidth);
        };
        /** @method generates dependencies that aren't intermediates **/
        this.genDeps = function (immups, immdowns) {
            let that = this;
            let ups = [];
            let downs = [];
            let currups = immups;
            let currdowns = immdowns;
            while (currups.length > 0 || currdowns.length > 0) {
                let newups = [];
                let newdowns = [];
                that.edges.map(function (edge) {
                    if (currups.includes(edge['destination'])) {
                        newups.push(edge['source']);
                        ups.push(edge['source']);
                    }
                    if (currdowns.includes(edge['source'])) {
                        newdowns.push(edge['destination']);
                        downs.push(edge['destination']);
                    }
                });
                currups = newups;
                currdowns = newdowns;
            }
            ups.map(function (up) {
                d3__WEBPACK_IMPORTED_MODULE_0__.select('#node' + up)
                    .classed('move_right', true)
                    .classed('active', true)
                    .classed('gray', true);
            });
            downs.map(function (down) {
                d3__WEBPACK_IMPORTED_MODULE_0__.select('#node' + down)
                    .classed('move_left', true)
                    .classed('active', true)
                    .classed('gray', true);
            });
        };
        /** @method activates the paths based on click **/
        this.elementActivate = function (parent, node) {
            let that = this;
            let ups = [];
            let downs = [];
            if (!node.classed('active_node')) {
                this.reset();
                node.classed('active_node', true);
                parent.classed('active', true);
                let activeId = parent.attr('id');
                activeId = activeId.substring(that.idSubstr.length, activeId.length);
                let sourceX = that.svgOffsetX;
                let offsetActive = 0;
                let sourceY = that.edgeYOffset + that.offsetX * that.orderFixed.indexOf(activeId);
                let uuid = activeId.substring(activeId.length - uuidLength, activeId.length);
                let immups = that.dfgraph.getImmUpstreams(uuid);
                let immdowns = that.dfgraph.getDownstreams(uuid);
                if (immups.length > 0 && immdowns.length > 0) {
                    sourceX = that.svgOffsetX - that.offsetActive / 2;
                    offsetActive = that.offsetActive;
                }
                else if (immups.length > 0) {
                    offsetActive = -(that.offsetActive / 2);
                }
                else if (immdowns.length > 0) {
                    offsetActive = that.offsetActive / 2;
                }
                let activeEle = '#node' + activeId;
                d3__WEBPACK_IMPORTED_MODULE_0__.select(activeEle)
                    .append('g')
                    .attr('transform', 'translate(0,0)')
                    .classed('activeedge', true)
                    .append('path')
                    .classed('source', true)
                    .attr('d', 'M' + sourceX + ' ' + sourceY + 'h ' + offsetActive)
                    .attr('stroke-width', that.strokeWidth)
                    .attr('fill', '#3b5fc0')
                    .attr('stroke', '#3b5fc0');
                d3__WEBPACK_IMPORTED_MODULE_0__.select('#text' + activeId).classed('active', true);
                if (that.mode == 'cells') {
                    this.tracker.currentWidget.content.activeCellIndex =
                        this.order.indexOf(activeId);
                }
                else {
                    this.tracker.currentWidget.content.activeCellIndex = this.order.indexOf(activeId.split(that.fixedIdentifier)[1]);
                }
                this.edges.map(function (edge) {
                    let source = edge['source'];
                    let destination = edge['destination'];
                    if (source == activeId) {
                        downs.push(destination);
                        let destinationNode = d3__WEBPACK_IMPORTED_MODULE_0__.select('#node' + destination)
                            .classed('move_left', true)
                            .classed('active', true)
                            .classed('imm', true);
                        let destCy = that.edgeYOffset +
                            that.offsetY * that.orderFixed.indexOf(destination);
                        that.makePaths(sourceY, destCy, parent, true);
                        destinationNode.selectAll('path.source').classed('hidden', true);
                    }
                    if (destination == activeId) {
                        ups.push(source);
                        let sourceNode = d3__WEBPACK_IMPORTED_MODULE_0__.select('#node' + source)
                            .classed('move_right', true)
                            .classed('active', true)
                            .classed('imm', true);
                        let srcCy = that.edgeYOffset + that.offsetY * that.orderFixed.indexOf(source);
                        that.makePaths(srcCy, sourceY, parent, false);
                        sourceNode.selectAll('path.destination').classed('hidden', true);
                    }
                });
            }
            that.genDeps(ups, downs);
            this.svg
                .selectAll('g')
                .filter(function (a) {
                return (!this.classList.contains('active') &&
                    this.parentElement.nodeName == 'svg');
            })
                .selectAll('path')
                .classed('hidden', true);
        };
        /** @method takes in a string id input and activates based on that ID*/
        this.updateActiveByID = function (activeid) {
            let sourceNode = null;
            let src = null;
            let that = this;
            if (this.mode == 'nodes') {
                let deps = this.dfgraph.getNodes(activeid);
                let addSpecifier = deps.length > 0 ? deps[0] : '';
                if (deps.length > 0 && deps[0] == undefined) {
                    addSpecifier = '';
                }
                sourceNode = d3__WEBPACK_IMPORTED_MODULE_0__.select('#node' + addSpecifier + that.fixedIdentifier + activeid)
                    .classed('move_right', true)
                    .classed('active', true);
                src = sourceNode.select('circle');
            }
            else {
                sourceNode = d3__WEBPACK_IMPORTED_MODULE_0__.select('#node' + activeid)
                    .classed('move_right', true)
                    .classed('active', true);
                src = sourceNode.select('circle');
            }
            this.elementActivate(sourceNode, src);
        };
        /** @method combines tags with respective uuids **/
        this.combineTags = function (uuid) {
            let that = this;
            if (uuid in this.outputTags) {
                if (this.dfgraph.getNodes(uuid).length == 0) {
                    return ['' + that.fixedIdentifier + uuid];
                }
                return this.outputTags[uuid].map((tag) => (tag ? tag : '') + that.fixedIdentifier + uuid);
            }
            return this.dfgraph.getNodes(uuid);
        };
        /** @method updateStates updates the states present in the graph */
        this.updateStates = function () {
            let that = this;
            that.svg
                .selectAll('rect.states')
                .data(that.orderFixed)
                .attr('fill', (uuid) => that.colormap[that.dfgraph.states[uuid.substring(uuid.length - uuidLength, uuid.length)] || 'None'])
                .enter()
                .append('rect')
                .attr('x', that.stateOffset)
                .attr('y', function (a, b) {
                return that.rectYOffset + that.offsetY * b;
            })
                .attr('width', that.statesWidth)
                .attr('height', that.statesHeight)
                .attr('rx', that.statesRx)
                .attr('ry', that.statesRy)
                .attr('id', (uuid) => 'state' + uuid)
                .attr('fill', (uuid) => that.colormap[that.dfgraph.states[uuid.substring(uuid.length - uuidLength, uuid.length)] || 'None'])
                .classed('states', true);
        };
        /** @method combines tags with respective uuids **/
        this.outTagsLength = function (uuid) {
            if (uuid in this.outputTags) {
                if (this.outputTags[uuid].length == 0) {
                    return 1;
                }
                return this.outputTags[uuid].length;
            }
            return 1;
        };
        /** @method grabs out tags from string **/
        this.grabOutTags = function (id, text) {
            let that = this;
            if (id in that.outputTags) {
                return that.outputTags[id].reduce((textobj, outputTag) => {
                    //FIXME: Make this smarter
                    let exp = new RegExp(outputTag);
                    if (!textobj) {
                        return '';
                    }
                    return textobj.replace(exp, 'OUTTAGSTARTSHERE' + outputTag + 'OUTTAGSTARTSHERE');
                }, text);
            }
            return text || '';
        };
        /** @method activates the paths based on click **/
        this.createMinimap = function (parent, node) {
            let that = this;
            let minitran = d3__WEBPACK_IMPORTED_MODULE_0__.transition().duration(0);
            let circles = this.svg.selectAll('circle');
            let data = null;
            if (that.mode == 'cells') {
                data = this.order;
            }
            else {
                data = this.order.reduce(function (a, b) {
                    return a.concat(that.combineTags(b));
                }, []);
            }
            let groups = circles
                .data(data, (a) => a)
                .enter()
                .append('g')
                //Have to use a proper start pattern for ID rules in HTML4
                .attr('id', (a) => 'node' + a);
            groups
                .append('rect')
                .attr('x', 0)
                .attr('y', (a, b) => 0 + b * that.offsetY)
                .attr('width', 500)
                .attr('height', that.offsetY)
                .attr('fill', 'transparent')
                .on('click', function () {
                let parent = d3__WEBPACK_IMPORTED_MODULE_0__.select(this.parentNode);
                let node = parent.select('circle');
                that.elementActivate(parent, node);
            });
            groups
                .append('circle')
                .transition(minitran)
                .attr('cx', this.svgOffsetX)
                .attr('cy', (a, b) => that.edgeYOffset + this.offsetY * b)
                .attr('r', this.radius);
            that.mapEdges(that);
            let values = this.order.map((a) => [
                a,
                that
                    .grabOutTags(a, that.getCellContents(a))
                    .split('OUTTAGSTARTSHERE')
                    .map((text) => {
                    return [text, (that.outputTags[a] || []).includes(text)];
                })
            ]);
            let textclick = function () {
                let id = d3__WEBPACK_IMPORTED_MODULE_0__.select(this).attr('id');
                id = id.substring(this.idSubstr.length, id.length);
                let parent = d3__WEBPACK_IMPORTED_MODULE_0__.select('#node' + id);
                let node = parent.select('circle');
                that.elementActivate(parent, node);
            };
            if (that.mode == 'nodes') {
                let fullSource = values;
                values = that.order.reduce(function (a, b) {
                    return a.concat(that
                        .getNodes(b)
                        .map((tag) => [
                        tag ? tag + that.fixedIdentifier + b : '',
                        [[tag, true]]
                    ]));
                }, []);
                let decoffset = 0;
                that.svg
                    .selectAll('rect.cells')
                    .data(that.order)
                    .enter()
                    .append('rect')
                    .classed('cells', true)
                    .attr('x', 8)
                    .attr('y', function (node) {
                    let curroffset = decoffset;
                    decoffset = decoffset + that.outTagsLength(node);
                    return that.rectYOffset + curroffset * that.offsetY;
                })
                    .attr('width', 50)
                    .attr('height', (node) => that.offsetY * that.outTagsLength(node) - that.rectYOffset)
                    .attr('rx', that.nodesRx)
                    .attr('ry', that.nodesRy);
                decoffset = 0;
                this.svg
                    .selectAll('text.source')
                    .data(fullSource, function (a) {
                    return a[0];
                })
                    .each(function (a) {
                    //For existing ones clear all text
                    //FIXME: This is a biproduct of not having full access to tags on load
                    jquery__WEBPACK_IMPORTED_MODULE_1___default()(this).empty();
                    d3__WEBPACK_IMPORTED_MODULE_0__.select(this)
                        .selectAll('tspan')
                        .data(a[1])
                        .enter()
                        .append('tspan')
                        .text(function (a) {
                        if (a[0]) {
                            return a[0];
                        }
                        return '';
                    })
                        .classed('outtag', (a) => a[1]);
                })
                    .on('click', textclick)
                    .enter()
                    .append('text')
                    .on('click', textclick)
                    .attr('id', (a) => 'text' + a[0])
                    .classed('source', true)
                    .attr('x', that.textOffset + that.svgOffsetX + 80)
                    .attr('y', function (a, b) {
                    let curroffset = decoffset;
                    let node = a[0];
                    let nodeLength = that.outTagsLength(node);
                    decoffset = decoffset + nodeLength;
                    if (nodeLength > 1) {
                        return (that.offsetY +
                            that.offsetY * curroffset +
                            that.offsetY / nodeLength);
                    }
                    return that.offsetY + that.offsetY * curroffset;
                })
                    .on('click', textclick)
                    .each(function (a) {
                    d3__WEBPACK_IMPORTED_MODULE_0__.select(this)
                        .selectAll('tspan')
                        .data(a[1])
                        .enter()
                        .append('tspan')
                        .text(function (a) {
                        if (a[0]) {
                            return a[0];
                        }
                        return '';
                    })
                        .classed('outtag', (a) => a[1]);
                });
                this.svg
                    .selectAll('rect.states')
                    .data(that.orderFixed)
                    .attr('fill', (uuid) => that.colormap[that.dfgraph.states[uuid.substring(uuid.length - 8, uuid.length)] || 'None'])
                    .enter()
                    .append('rect')
                    .attr('x', that.stateOffset)
                    .attr('y', function (a, b) {
                    return that.rectYOffset + that.offsetY * b;
                })
                    .attr('width', '5px')
                    .attr('height', '12px')
                    .attr('rx', '2px')
                    .attr('ry', '2px')
                    .attr('id', (uuid) => 'state' + uuid)
                    .attr('fill', function (uuid) {
                    return that.colormap[that.dfgraph.states[uuid.substring(uuid.length - 8, uuid.length)] ||
                        'None'];
                })
                    .classed('states', true);
            }
            this.svg
                .selectAll('text.labels')
                .data(values, function (a) {
                return a[0];
            })
                .each(function (a) {
                //For existing ones clear all text
                //FIXME: This is a biproduct of not having full access to tags on load
                jquery__WEBPACK_IMPORTED_MODULE_1___default()(this).empty();
                d3__WEBPACK_IMPORTED_MODULE_0__.select(this)
                    .selectAll('tspan')
                    .data(a[1])
                    .enter()
                    .append('tspan')
                    .text(function (a) {
                    if (a[0]) {
                        return a[0].length > that.textEllide
                            ? a[0].substring(0, 7) + '..'
                            : a[0];
                    }
                    return '';
                })
                    .classed('outtag', (a) => a[1]);
            })
                .on('click', textclick)
                .enter()
                .append('text')
                .on('click', textclick)
                .attr('id', (a) => 'text' + a[0])
                .attr('x', this.textOffset + this.svgOffsetX)
                .attr('y', (a, b) => that.offsetY + this.offsetY * b)
                .each(function (a) {
                jquery__WEBPACK_IMPORTED_MODULE_1___default()(this).empty();
                d3__WEBPACK_IMPORTED_MODULE_0__.select(this)
                    .selectAll('tspan')
                    .data(a[1])
                    .enter()
                    .append('tspan')
                    .text(function (a) {
                    if (a[0]) {
                        return a[0].length > that.textEllide
                            ? a[0].substring(0, 7) + '..'
                            : a[0];
                    }
                    return '';
                })
                    .classed('outtag', (a) => a[1]);
            })
                .classed('labels', true);
        };
        /** @method this method is mostly here to make sure we return something for display purposes **/
        this.getNodes = function (uuid) {
            let nodes = this.dfgraph.getNodes(uuid);
            if (nodes.length == 0) {
                return [''];
            }
            return nodes;
        };
        /** @method maps edges to incoming and outgoing paths in the svg **/
        this.mapEdges = function (parent, node) {
            let that = this;
            if (that.mode == 'cells') {
                that.orderFixed = this.order;
            }
            else {
                that.orderFixed = this.order.reduce(function (a, b) {
                    return a.concat(that.combineTags(b));
                }, []);
            }
            let edgelist = {}; //:;
            this.edges.map(function (edge) {
                let sourceId = '#node' + edge['source'];
                let destinationId = '#node' + edge['destination'];
                if (sourceId in edgelist) {
                    if (edgelist[sourceId].includes(destinationId)) {
                        return;
                    }
                    edgelist[sourceId].push(destinationId);
                }
                else {
                    edgelist[sourceId] = [destinationId];
                }
                let sourceX = that.svgOffsetX;
                let sourceY = that.edgeYOffset +
                    that.offsetX * that.orderFixed.indexOf(edge['source']);
                let destinationX = that.svgOffsetX;
                let destinationY = that.edgeYOffset +
                    that.offsetX * that.orderFixed.indexOf(edge['destination']);
                d3__WEBPACK_IMPORTED_MODULE_0__.select(sourceId)
                    .append('g')
                    .attr('transform', 'translate(0,0)')
                    .attr('id', 'edge' + edge['source'])
                    .append('path')
                    .classed('source', true)
                    .attr('d', 'M' + sourceX + ' ' + sourceY + 'h 8')
                    .attr('stroke-width', that.strokeWidth)
                    .attr('fill', 'none')
                    .attr('stroke', 'black');
                d3__WEBPACK_IMPORTED_MODULE_0__.select(destinationId)
                    .append('g')
                    .attr('transform', 'translate(0,0)')
                    .attr('id', 'edge' + edge['source'])
                    .append('path')
                    .classed('destination', true)
                    .attr('d', 'M' + destinationX + ' ' + destinationY + 'h -8')
                    .attr('stroke-width', that.strokeWidth)
                    .attr('fill', 'none')
                    .attr('stroke', 'black');
            });
        };
        /** @method get cell contents if not in graph **/
        this.getCellContents = function (uuid) {
            let that = this;
            if (uuid in that.cells) {
                return that.cells[uuid];
            }
            let splitCell = that.dfgraph.getText(uuid).split('\n');
            let cellContent = splitCell[splitCell.length - 1];
            that.cells[uuid] = cellContent || '';
            return that.cells[uuid];
        };
        /** @method changes cell contents **/
        // Always call before any updates to graph
        this.updateCells = function () {
            let that = this;
            that.cells = Object.keys(this.dfgraph.cellContents).reduce(function (a, b) {
                let splitCell = that.dfgraph.cellContents[b].split('\n');
                a[b] = splitCell[splitCell.length - 1];
                return a;
            }, {});
            that.updateOrder(that.tracker.currentWidget.model.cells.model.cells.map((cell) => cell.id));
            return true;
        };
        /** @method updates the edges in the minimap */
        //Always call before any updates to graph
        this.updateEdges = function () {
            let that = this;
            if (this.mode == 'cells') {
                const flatten = (arr) => arr.reduce((flat, next) => flat.concat(next), []);
                let edges = that.dfgraph.downlinks;
                that.edges = flatten(Object.keys(edges).map(function (edge) {
                    return edges[edge].map(function (dest) {
                        return { source: edge, destination: dest };
                    });
                }));
            }
            else {
                that.edges = [];
                let cells = that.dfgraph.getCells();
                that.cellLinks = [];
                that.outputNodes = [];
                cells.forEach(function (uuid) {
                    that.outputNodes[uuid] = that.getNodes(uuid);
                    let outnames = that.outputNodes[uuid];
                    that.dfgraph.getUpstreams(uuid).forEach(function (b) {
                        let sUuid = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_2__.truncateCellId)(b);
                        let sNode = b.substring(uuidLength, b.length);
                        outnames.forEach((out) => {
                            that.edges.push({
                                source: sNode + that.fixedIdentifier + sUuid,
                                destination: out + that.fixedIdentifier + uuid
                            });
                        });
                    });
                });
            }
            return true;
        };
        /** @method creates the starting environment for first time setup*/
        this.createMiniArea = function () {
            (async () => {
                while (jquery__WEBPACK_IMPORTED_MODULE_1___default()('#minisvg').height() === 0)
                    // wait until the main div has a size to do anything
                    await new Promise(resolve => setTimeout(resolve, 100));
                d3__WEBPACK_IMPORTED_MODULE_0__.select('#minimap').classed('container', true);
                let that = this;
                this.svg = d3__WEBPACK_IMPORTED_MODULE_0__.select('#minisvg');
                this.svg = this.svg.append('g');
                this.svg.attr('transform', 'translate(0,0)');
                this.toggle = d3__WEBPACK_IMPORTED_MODULE_0__.select('#minimap')
                    .append('div')
                    .attr('id', 'side-panel-mini');
                this.tabular = this.toggle
                    .append('div')
                    .attr('id', 'table')
                    .classed('card', true);
                let label = this.tabular.append('label').classed('switch', true);
                label
                    .append('input')
                    .attr('type', 'checkbox')
                    .on('change', function () {
                    that.changeMode();
                });
                label.append('span').classed('slider', true).classed('round', true);
                this.startMinimapCreation();
            })();
        };
        /** @method clear graph */
        this.clearMinimap = function () {
            jquery__WEBPACK_IMPORTED_MODULE_1___default()('#minisvg g').empty();
        };
        /** @method updates the list of output tags on the graph */
        this.updateOutputTags = function () {
            let that = this;
            that.outputTags = {};
            that.dfgraph.getCells().forEach(function (uuid) {
                that.outputTags[uuid] = that.dfgraph.getNodes(uuid);
            });
            return true;
        };
        /** @method starts minimap creation, this is the process that's ran every time **/
        this.startMinimapCreation = function () {
            if (this.updateCells() && this.updateOutputTags() && this.updateEdges()) {
                let that = this;
                that.createMinimap();
            }
        };
        /** @method changes the current mode in which the minimap is being displayed */
        this.changeMode = function () {
            let that = this;
            that.mode = that.mode == 'nodes' ? 'cells' : 'nodes';
            that.clearMinimap();
            that.startMinimapCreation();
        };
        /** @method set graph, sets the current activate graph to be visualized */
        this.setGraph = function (graph) {
            this.dfgraph = graph;
            this.updateOrder(this.tracker.currentWidget.model.cells.model.cells.map((cell) => cell.id));
            if (this.svg) {
                this.clearMinimap();
                this.startMinimapCreation();
            }
        };
        this.wasCreated = false;
        this.radius = 3;
        this.offsetX = 15;
        this.offsetY = 15;
        this.svgOffsetX = 32;
        this.svgOffsetY = 50;
        this.textOffset = 40;
        this.stateOffset = 63;
        this.pathOffset = 8;
        this.edgeYOffset = 10;
        this.strokeWidth = 2;
        this.offsetActive = 24;
        this.rectYOffset = 4;
        this.statesWidth = 5;
        this.statesHeight = 12;
        this.nodesRx = this.nodesRy = 3;
        this.statesRx = this.statesRy = 2;
        //Elides text after this length
        this.textEllide = 10;
        this.idSubstr = 'node';
        this.fixedIdentifier = 'DFELEMENT';
        this.cells = {};
        this.parentdiv = parentdiv || '#minimap';
        this.edges = [];
        this.outputTags = {};
        this.dfgraph = dfgraph || null;
        this.tracker = null;
        this.toggle = null;
        this.tabular = null;
        //this.mode = 'cells';
        this.mode = 'nodes';
        this.colormap = {
            Stale: 'yellow',
            Fresh: 'blue',
            'Upstream Stale': 'yellow',
            Changed: 'orange',
            None: 'grey'
        };
        //this.widget =
    }
}


/***/ }),

/***/ "../dfgraph/lib/viewer.js":
/*!********************************!*\
  !*** ../dfgraph/lib/viewer.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ViewerWidget: () => (/* binding */ ViewerWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);

/**
 * A class for all ViewerWidgets, allows tracking of if they're open or not.
 */
class ViewerWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        super();
        this.isOpen = false;
    }
    //We can track our ViewerWidget events by subclassing Lumino Widgets
    /**
     * Handle a `after-attach` message.
     */
    onAfterAttach() {
        this.isOpen = true;
    }
    /**
     * Handle a `after-detach` message.
     */
    onAfterDetach() {
        this.isOpen = false;
    }
}


/***/ })

}]);
//# sourceMappingURL=dfgraph_lib_index_js.4715a6031daa5a935a79.js.map