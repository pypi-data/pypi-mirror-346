"use strict";
(self["webpackChunk_dfnotebook_dfnotebook_extension"] = self["webpackChunk_dfnotebook_dfnotebook_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/cellexecutor.js":
/*!*****************************!*\
  !*** ./lib/cellexecutor.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   cellExecutor: () => (/* binding */ cellExecutor)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @dfnotebook/dfnotebook */ "webpack/sharing/consume/default/@dfnotebook/dfnotebook/@dfnotebook/dfnotebook");
/* harmony import */ var _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * Notebook cell executor plugin.
 */
const cellExecutor = {
    id: '@dfnotebook/dfnotebook-extension:cell-executor',
    description: 'Provides the notebook cell executor.',
    autoStart: true,
    provides: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookCellExecutor,
    activate: () => {
        return Object.freeze({ runCell: _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_1__.runCell });
    }
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   tagIcon: () => (/* binding */ tagIcon),
/* harmony export */   updateNotebookCellsWithTag: () => (/* binding */ updateNotebookCellsWithTag)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @dfnotebook/dfgraph */ "webpack/sharing/consume/default/@dfnotebook/dfgraph/@dfnotebook/dfgraph");
/* harmony import */ var _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_docmanager_extension__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/docmanager-extension */ "webpack/sharing/consume/default/@jupyterlab/docmanager-extension");
/* harmony import */ var _jupyterlab_docmanager_extension__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager_extension__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @dfnotebook/dfutils */ "webpack/sharing/consume/default/@dfnotebook/dfutils/@dfnotebook/dfutils");
/* harmony import */ var _dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_15___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_15__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_16___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_16__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_17___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_17__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_18___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_18__);
/* harmony import */ var _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @dfnotebook/dfnotebook */ "webpack/sharing/consume/default/@dfnotebook/dfnotebook/@dfnotebook/dfnotebook");
/* harmony import */ var _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_19___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_19__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_20___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_20__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_21___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_21__);
/* harmony import */ var _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! @dfnotebook/dfcells */ "webpack/sharing/consume/default/@dfnotebook/dfcells/@dfnotebook/dfcells");
/* harmony import */ var _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_22___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_22__);
/* harmony import */ var _cellexecutor__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! ./cellexecutor */ "./lib/cellexecutor.js");
/* harmony import */ var _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! @jupyterlab/cell-toolbar */ "webpack/sharing/consume/default/@jupyterlab/cell-toolbar");
/* harmony import */ var _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_23___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_23__);
/* harmony import */ var _style_tag_svg__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! ../style/tag.svg */ "./style/tag.svg");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module dfnotebook-extension
 */



























const tagIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.LabIcon({
    name: 'tag',
    svgstr: _style_tag_svg__WEBPACK_IMPORTED_MODULE_24__
});
/**
 * The command IDs used by the notebook plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.createNew = 'notebook:create-new';
    CommandIDs.interrupt = 'notebook:interrupt-kernel';
    CommandIDs.restart = 'notebook:restart-kernel';
    CommandIDs.restartClear = 'notebook:restart-clear-output';
    CommandIDs.restartAndRunToSelected = 'notebook:restart-and-run-to-selected';
    CommandIDs.restartRunAll = 'notebook:restart-run-all';
    CommandIDs.reconnectToKernel = 'notebook:reconnect-to-kernel';
    CommandIDs.changeKernel = 'notebook:change-kernel';
    CommandIDs.getKernel = 'notebook:get-kernel';
    CommandIDs.createConsole = 'notebook:create-console';
    CommandIDs.createOutputView = 'notebook:create-output-view';
    CommandIDs.clearAllOutputs = 'notebook:clear-all-cell-outputs';
    CommandIDs.shutdown = 'notebook:shutdown-kernel';
    CommandIDs.closeAndShutdown = 'notebook:close-and-shutdown';
    CommandIDs.trust = 'notebook:trust';
    CommandIDs.exportToFormat = 'notebook:export-to-format';
    CommandIDs.run = 'notebook:run-cell';
    CommandIDs.runAndAdvance = 'notebook:run-cell-and-select-next';
    CommandIDs.runAndInsert = 'notebook:run-cell-and-insert-below';
    CommandIDs.runInConsole = 'notebook:run-in-console';
    CommandIDs.runAll = 'notebook:run-all-cells';
    CommandIDs.runAllAbove = 'notebook:run-all-above';
    CommandIDs.runAllBelow = 'notebook:run-all-below';
    CommandIDs.renderAllMarkdown = 'notebook:render-all-markdown';
    CommandIDs.toCode = 'notebook:change-cell-to-code';
    CommandIDs.toMarkdown = 'notebook:change-cell-to-markdown';
    CommandIDs.toRaw = 'notebook:change-cell-to-raw';
    CommandIDs.cut = 'notebook:cut-cell';
    CommandIDs.copy = 'notebook:copy-cell';
    CommandIDs.pasteAbove = 'notebook:paste-cell-above';
    CommandIDs.pasteBelow = 'notebook:paste-cell-below';
    CommandIDs.duplicateBelow = 'notebook:duplicate-below';
    CommandIDs.pasteAndReplace = 'notebook:paste-and-replace-cell';
    CommandIDs.moveUp = 'notebook:move-cell-up';
    CommandIDs.moveDown = 'notebook:move-cell-down';
    CommandIDs.clearOutputs = 'notebook:clear-cell-output';
    CommandIDs.deleteCell = 'notebook:delete-cell';
    CommandIDs.insertAbove = 'notebook:insert-cell-above';
    CommandIDs.insertBelow = 'notebook:insert-cell-below';
    CommandIDs.selectAbove = 'notebook:move-cursor-up';
    CommandIDs.selectBelow = 'notebook:move-cursor-down';
    CommandIDs.selectHeadingAboveOrCollapse = 'notebook:move-cursor-heading-above-or-collapse';
    CommandIDs.selectHeadingBelowOrExpand = 'notebook:move-cursor-heading-below-or-expand';
    CommandIDs.insertHeadingAbove = 'notebook:insert-heading-above';
    CommandIDs.insertHeadingBelow = 'notebook:insert-heading-below';
    CommandIDs.extendAbove = 'notebook:extend-marked-cells-above';
    CommandIDs.extendTop = 'notebook:extend-marked-cells-top';
    CommandIDs.extendBelow = 'notebook:extend-marked-cells-below';
    CommandIDs.extendBottom = 'notebook:extend-marked-cells-bottom';
    CommandIDs.selectAll = 'notebook:select-all';
    CommandIDs.deselectAll = 'notebook:deselect-all';
    CommandIDs.editMode = 'notebook:enter-edit-mode';
    CommandIDs.merge = 'notebook:merge-cells';
    CommandIDs.mergeAbove = 'notebook:merge-cell-above';
    CommandIDs.mergeBelow = 'notebook:merge-cell-below';
    CommandIDs.split = 'notebook:split-cell-at-cursor';
    CommandIDs.commandMode = 'notebook:enter-command-mode';
    CommandIDs.toggleAllLines = 'notebook:toggle-all-cell-line-numbers';
    CommandIDs.undoCellAction = 'notebook:undo-cell-action';
    CommandIDs.redoCellAction = 'notebook:redo-cell-action';
    CommandIDs.redo = 'notebook:redo';
    CommandIDs.undo = 'notebook:undo';
    CommandIDs.markdown1 = 'notebook:change-cell-to-heading-1';
    CommandIDs.markdown2 = 'notebook:change-cell-to-heading-2';
    CommandIDs.markdown3 = 'notebook:change-cell-to-heading-3';
    CommandIDs.markdown4 = 'notebook:change-cell-to-heading-4';
    CommandIDs.markdown5 = 'notebook:change-cell-to-heading-5';
    CommandIDs.markdown6 = 'notebook:change-cell-to-heading-6';
    CommandIDs.hideCode = 'notebook:hide-cell-code';
    CommandIDs.showCode = 'notebook:show-cell-code';
    CommandIDs.hideAllCode = 'notebook:hide-all-cell-code';
    CommandIDs.showAllCode = 'notebook:show-all-cell-code';
    CommandIDs.hideOutput = 'notebook:hide-cell-outputs';
    CommandIDs.showOutput = 'notebook:show-cell-outputs';
    CommandIDs.hideAllOutputs = 'notebook:hide-all-cell-outputs';
    CommandIDs.showAllOutputs = 'notebook:show-all-cell-outputs';
    CommandIDs.toggleRenderSideBySideCurrentNotebook = 'notebook:toggle-render-side-by-side-current';
    CommandIDs.setSideBySideRatio = 'notebook:set-side-by-side-ratio';
    CommandIDs.enableOutputScrolling = 'notebook:enable-output-scrolling';
    CommandIDs.disableOutputScrolling = 'notebook:disable-output-scrolling';
    CommandIDs.selectLastRunCell = 'notebook:select-last-run-cell';
    CommandIDs.replaceSelection = 'notebook:replace-selection';
    CommandIDs.autoClosingBrackets = 'notebook:toggle-autoclosing-brackets';
    CommandIDs.toggleCollapseCmd = 'notebook:toggle-heading-collapse';
    CommandIDs.collapseAllCmd = 'notebook:collapse-all-headings';
    CommandIDs.expandAllCmd = 'notebook:expand-all-headings';
    CommandIDs.copyToClipboard = 'notebook:copy-to-clipboard';
    CommandIDs.invokeCompleter = 'completer:invoke-notebook';
    CommandIDs.selectCompleter = 'completer:select-notebook';
    CommandIDs.tocRunCells = 'toc:run-cells';
    CommandIDs.addCellTag = 'notebook:add-cell-tag';
    CommandIDs.modifyCellTag = 'notebook:modify-cell-tag';
    CommandIDs.tagCodeCell = 'toolbar-button:tag-cell';
})(CommandIDs || (CommandIDs = {}));
/**
 * The name of the factory that creates notebooks.
 */
const FACTORY = 'Notebook';
/**
 * The name of the factory that creates dataflow notebooks.
 */
const DATAFLOW_FACTORY = 'Dataflow Notebook';
/**
 * Setting Id storing the customized toolbar definition.
 */
const PANEL_SETTINGS = '@jupyterlab/notebook-extension:panel';
/**
 * The id to use on the style tag for the side by side margins.
 */
const SIDE_BY_SIDE_STYLE_ID = 'jp-NotebookExtension-sideBySideMargins';
/**
 * The notebook widget tracker provider.
 */
const trackerPlugin = {
    id: '@dfnotebook/dfnotebook-extension:tracker',
    description: 'Provides the notebook widget tracker.',
    provides: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.INotebookTracker,
    requires: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.INotebookWidgetFactory,
        _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_19__.IDataflowNotebookWidgetFactory,
        _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_5__.IEditorExtensionRegistry,
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.INotebookCellExecutor
    ],
    optional: [
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_7__.IDefaultFileBrowser,
        _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_8__.ILauncher,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_9__.IMainMenu,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__.ISettingRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator,
        _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.IFormRendererRegistry
    ],
    activate: activateNotebookHandler,
    autoStart: true
};
/**
 * The dataflow notebook cell factory provider.
 */
const factory = {
    id: '@dfnotebook/dfnotebook-extension:factory',
    description: 'Provides the dataflow notebook cell factory.',
    provides: _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_19__.DataflowNotebookPanel.IContentFactory,
    requires: [_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4__.IEditorServices],
    autoStart: true,
    activate: (app, editorServices) => {
        const editorFactory = editorServices.factoryService.newInlineEditor;
        return new _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_19__.DataflowNotebookPanel.ContentFactory({ editorFactory });
    }
};
/**
 * The dataflow notebook widget factory provider.
 */
const widgetFactoryPlugin = {
    id: '@dfnotebook/dfnotebook-extension:widget-factory',
    description: 'Provides the dataflow notebook widget factory.',
    provides: _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_19__.IDataflowNotebookWidgetFactory,
    requires: [
        _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_19__.DataflowNotebookPanel.IContentFactory,
        _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4__.IEditorServices,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_20__.IRenderMimeRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IToolbarWidgetRegistry
    ],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    activate: activateDataflowWidgetFactory,
    autoStart: true
};
// FIXME Add back when dfgraph is updated
// /**
//  * Initialization for the Dfnb GraphManager for working with multiple graphs.
//  */
const GraphManagerPlugin = {
    id: 'dfnb-graph',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.INotebookTracker],
    activate: (app, palette, nbTrackers) => {
        // Create a blank content widget inside of a MainAreaWidget
        console.log("GraphManager is active");
        let shell = app.shell;
        nbTrackers.widgetAdded.connect((sender, nbPanel) => {
            const session = nbPanel.sessionContext;
            _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.setTracker(nbTrackers);
            session.ready.then(() => {
                var _a, _b, _c;
                let outputTags = {};
                let cellContents = {};
                let cellList = (_b = (_a = nbPanel.model) === null || _a === void 0 ? void 0 : _a.toJSON()) === null || _b === void 0 ? void 0 : _b.cells;
                cellList.map(function (cell) {
                    let cellId = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_10__.truncateCellId)(cell.id);
                    if ((cell === null || cell === void 0 ? void 0 : cell.cell_type) != "code") {
                        return;
                    }
                    cellContents[cellId] = cell.source;
                    outputTags[cellId] =
                        (cell === null || cell === void 0 ? void 0 : cell.outputs).flatMap((output) => { var _a, _b; return ((_b = (_a = output === null || output === void 0 ? void 0 : output.metadata) === null || _a === void 0 ? void 0 : _a.output_tag) !== null && _b !== void 0 ? _b : []); });
                });
                let cells = Object.keys(outputTags);
                let uplinks = cells.reduce((dict, cellId) => { dict[cellId] = {}; return dict; }, {});
                let downlinks = cells.reduce((dict, cellId) => { dict[cellId] = []; return dict; }, {});
                Object.keys(cellContents).map(function (cellId) {
                    let regex = /\w+\$[a-f0-9]{8}/g;
                    let references = (cellContents[cellId].match(regex)) || [];
                    references.map(function (reference) {
                        let ref = reference.split('$');
                        if (ref[1] in uplinks[cellId]) {
                            uplinks[cellId][ref[1]].push(ref[0]);
                        }
                        else {
                            uplinks[cellId][ref[1]] = [ref[0]];
                        }
                        downlinks[ref[1]].push(cellId);
                    });
                });
                let sessId = ((_c = session === null || session === void 0 ? void 0 : session.session) === null || _c === void 0 ? void 0 : _c.id) || "None";
                if (!(sessId in Object.keys(_dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.graphs))) {
                    //@ts-ignore
                    _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.graphs[sessId] = new _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Graph({ 'cells': cells, 'nodes': outputTags, 'internalNodes': outputTags, 'uplinks': uplinks, 'downlinks': downlinks, 'cellContents': cellContents });
                    _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.updateGraph(sessId);
                    let cellOrder = cellList.map((c) => c.id);
                    _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.updateOrder(cellOrder);
                }
                console.log(sessId);
            });
            nbPanel.content.model._cells.changed.connect(() => {
                _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.updateOrder(nbPanel.content.model.cells.model.cells.map((cell) => cell.id));
            });
            nbPanel.content.activeCellChanged.connect(() => {
                var _a, _b, _c;
                let prevActive = _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.getActive();
                if (typeof prevActive == 'object' && prevActive.id != undefined) {
                    let uuid = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_10__.truncateCellId)(prevActive.id);
                    if (prevActive.sharedModel.source != _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.getText(uuid)) {
                        _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.markStale(uuid);
                    }
                    else if (_dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.getStale(uuid) == 'Stale') {
                        _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.revertStale(uuid);
                    }
                }
                //Have to get this off the model the same way that actions.tsx does
                let activeId = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_10__.truncateCellId)(((_b = (_a = nbPanel.content.activeCell) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.id.replace(/-/g, '')) || '');
                _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.updateActive(activeId, (_c = nbPanel.content.activeCell) === null || _c === void 0 ? void 0 : _c.model);
            });
        });
        shell.currentChanged.connect((_, change) => {
            var _a, _b, _c;
            //@ts-ignore
            let sessId = (_c = (_b = (_a = change['newValue']) === null || _a === void 0 ? void 0 : _a.sessionContext) === null || _b === void 0 ? void 0 : _b.session) === null || _c === void 0 ? void 0 : _c.id;
            if (sessId in _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.graphs) {
                _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.updateActiveGraph();
            }
        });
    }
};
// /**
//  * Initialization data for the Dfnb Depviewer extension.
//  */
const DepViewer = {
    id: 'dfnb-depview',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.INotebookTracker],
    activate: (app, palette, nbTrackers) => {
        // Create a blank content widget inside of a MainAreaWidget
        const newWidget = () => {
            const content = new _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.ViewerWidget();
            //GraphManager uses flags from the ViewerWidget
            _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.depWidget = content;
            const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
            widget.id = 'dfnb-depview';
            widget.title.label = 'Dependency Viewer';
            widget.title.closable = true;
            // Add a div to the panel
            let panel = document.createElement('div');
            panel.setAttribute('id', 'depview');
            content.node.appendChild(panel);
            return widget;
        };
        let widget = newWidget();
        function openDepViewer() {
            if (widget.isDisposed) {
                widget = newWidget();
                _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.depview.isCreated = false;
            }
            if (!widget.isAttached) {
                // Attach the widget to the main work area if it's not there
                app.shell.add(widget, 'main', {
                    mode: 'split-right',
                    activate: false
                });
                if (!_dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.depview.isCreated) {
                    _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.depview.createDepDiv();
                }
            }
            // Activate the widget
            app.shell.activateById(widget.id);
            _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.depview.isOpen = true;
            _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.depview.startGraphCreation();
        }
        nbTrackers.widgetAdded.connect((sender, nbPanel) => {
            const session = nbPanel.sessionContext;
            session.ready.then(() => {
                var _a, _b;
                if (((_b = (_a = session.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.name) == 'dfpython3') {
                    const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
                        className: 'open-dep-view',
                        label: 'Open Dependency Viewer',
                        onClick: openDepViewer,
                        tooltip: 'Opens the Dependency Viewer',
                    });
                    nbPanel.toolbar.insertItem(10, 'Open Dependency Viewer', button);
                }
            });
        });
        // Add an application command
        const command = 'depview:open';
        app.commands.addCommand(command, {
            label: 'Open Dependency Viewer',
            execute: () => openDepViewer,
        });
        // Add the command to the palette.
        palette.addItem({ command, category: 'Tutorial' });
    }
};
// /**
//  * Initialization data for the Minimap extension.
//  */
const MiniMap = {
    id: 'dfnb-minimap',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.INotebookTracker],
    activate: (app, palette, nbTrackers) => {
        const newWidget = () => {
            const content = new _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.ViewerWidget();
            //Graph Manager maintains the flags on the widgets
            _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.miniWidget = content;
            const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
            widget.id = 'dfnb-minimap';
            widget.title.label = 'Notebook Minimap';
            widget.title.closable = true;
            // Add a div to the panel
            let panel = document.createElement('div');
            panel.setAttribute('id', 'minimap');
            let inner = document.createElement('div');
            inner.setAttribute('id', 'minidiv');
            let svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            svg.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
            svg.setAttribute('id', 'minisvg');
            inner.append(svg);
            panel.appendChild(inner);
            content.node.appendChild(panel);
            return widget;
        };
        let widget = newWidget();
        nbTrackers.widgetAdded.connect((sender, nbPanel) => {
            const session = nbPanel.sessionContext;
            session.ready.then(() => {
                var _a, _b;
                if (((_b = (_a = session.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.name) == 'dfpython3') {
                    const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
                        className: 'open-mini-map',
                        label: 'Open Minimap',
                        onClick: openMinimap,
                        tooltip: 'Opens the Minimap',
                    });
                    nbPanel.toolbar.insertItem(10, 'Open Minimap', button);
                }
            });
        });
        function openMinimap() {
            if (widget.isDisposed) {
                widget = newWidget();
                _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.minimap.wasCreated = false;
            }
            if (!widget.isAttached) {
                app.shell.add(widget, 'main', {
                    mode: 'split-right',
                    activate: false
                });
                //'right');
                if (!_dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.minimap.wasCreated) {
                    console.log("Active Graph", _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.graphs[_dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.currentGraph]);
                    // Activate the widget
                    app.shell.activateById(widget.id);
                    _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.minimap.createMiniArea();
                    _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.minimap.wasCreated = true;
                }
                else {
                    _dfnotebook_dfgraph__WEBPACK_IMPORTED_MODULE_2__.Manager.minimap.startMinimapCreation();
                }
            }
        }
        // Add an application command
        const command = 'minimap:open';
        app.commands.addCommand(command, {
            label: 'Open Minimap',
            execute: () => openMinimap,
        });
        // Add the command to the palette.
        palette.addItem({ command, category: 'Tutorial' });
    }
};
const cellToolbar = {
    id: '@dfnotebook/dfnotebook-extension:cell-toolbar',
    description: 'Add the cells toolbar.',
    autoStart: true,
    activate: async (app, settingRegistry, toolbarRegistry, translator) => {
        const toolbarItems = settingRegistry && toolbarRegistry
            ? (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.createToolbarFactory)(toolbarRegistry, settingRegistry, _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_23__.CellBarExtension.FACTORY_NAME, '@jupyterlab/cell-toolbar-extension:plugin', translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.nullTranslator)
            : undefined;
        // have to register this with our factory
        app.docRegistry.addWidgetExtension(DATAFLOW_FACTORY, new _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_23__.CellBarExtension(app.commands, toolbarItems));
    },
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IToolbarWidgetRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator]
};
/**
 * Creates the toggle switch used for hiding/showing tags
 */
class ToggleTagsWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_18__.Widget {
    constructor(nbPanel, app) {
        super();
        this.addClass('jupyter-toggle-switch-widget');
        const containerDiv = document.createElement('div');
        containerDiv.className = 'toggle-container';
        const labelText = document.createElement('span');
        labelText.textContent = 'Tags';
        labelText.className = 'toggle-label';
        const label = document.createElement('label');
        label.className = 'switch';
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.checked = true;
        const slider = document.createElement('span');
        slider.className = 'slider round';
        label.appendChild(input);
        label.appendChild(slider);
        containerDiv.appendChild(labelText);
        containerDiv.appendChild(label);
        const updateTooltip = (isChecked) => {
            const tooltipText = isChecked ? `Toggle to hide the tags in the notebook` : `Toggle to show the tags in the notebook`;
            label.title = tooltipText;
            labelText.title = tooltipText;
            slider.title = tooltipText;
        };
        updateTooltip(true);
        updateNotebookCellsWithTag(nbPanel.id, nbPanel.model, "", nbPanel.sessionContext);
        input.addEventListener('change', async (event) => {
            var _a;
            const isChecked = event.target.checked;
            const notebook = nbPanel.content;
            const cellsArray = Array.from(notebook.widgets);
            updateTooltip(isChecked);
            cellsArray.forEach(cAny => {
                const dfmetadata = cAny.model.getMetadata('dfmetadata');
                if (cAny.model.type == 'code' && dfmetadata.tag) {
                    const inputArea = cAny.inputArea;
                    let currTag = dfmetadata.tag;
                    if (isChecked) {
                        inputArea.addTag(currTag);
                    }
                    else {
                        inputArea.addTag("");
                        dfmetadata.tag = currTag;
                        cAny.model.setMetadata('dfmetadata', dfmetadata);
                    }
                }
            });
            (_a = nbPanel.model) === null || _a === void 0 ? void 0 : _a.setMetadata("enable_tags", isChecked);
            app.commands.notifyCommandChanged('toolbar-button:tag-cell');
            await updateNotebookCellsWithTag(nbPanel.id, nbPanel.model, "", nbPanel.sessionContext, !isChecked);
        });
        this.node.appendChild(containerDiv);
    }
}
/**
 * Adds Tags toggle switch in frontend toolbar for dfkernels notebooks
 */
const ToggleTags = {
    id: 'toggle-tags',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.INotebookTracker],
    activate: (app, nbTrackers) => {
        nbTrackers.widgetAdded.connect((sender, nbPanel) => {
            const session = nbPanel.sessionContext;
            session.ready.then(async () => {
                var _a, _b;
                if (((_b = (_a = session.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.name) == 'dfpython3') {
                    const toggleSwitch = new ToggleTagsWidget(nbPanel, app);
                    nbPanel.toolbar.insertItem(12, 'customToggleTag', toggleSwitch);
                }
            });
        });
    }
};
const NotebookCellTrackerPlugin = {
    id: 'notebook-cell-tracker',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.INotebookTracker],
    activate: (app, tracker) => {
        tracker.widgetAdded.connect((_, notebookPanel) => {
            const notebookModel = notebookPanel.content.model;
            if (!notebookModel) {
                console.warn('Notebook model not found.');
                return;
            }
            const notebookId = notebookPanel.id;
            if (!_dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_22__.notebookCellMap.has(notebookId)) {
                _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_22__.notebookCellMap.set(notebookId, new Map());
            }
            const cellMap = _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_22__.notebookCellMap.get(notebookId);
            notebookModel.cells.changed.connect((_, changes) => {
                if (changes.type === 'add') {
                    for (const cell of changes.newValues) {
                        if (cell.type === 'code') {
                            const codeCell = cell;
                            const cellId = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_10__.truncateCellId)(codeCell.id);
                            cellMap.set(cellId, codeCell.sharedModel.getSource());
                        }
                    }
                }
                else if (changes.type === 'remove') {
                    for (const deletedCellId of notebookModel.deletedCells) {
                        const cellId = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_10__.truncateCellId)(deletedCellId);
                        cellMap.delete(cellId);
                    }
                }
            });
            //notebook closed
            notebookPanel.disposed.connect(() => {
                _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_22__.notebookCellMap.delete(notebookId);
            });
        });
    }
};
const plugins = [
    _cellexecutor__WEBPACK_IMPORTED_MODULE_25__.cellExecutor,
    factory,
    widgetFactoryPlugin,
    trackerPlugin,
    cellToolbar,
    DepViewer,
    MiniMap,
    GraphManagerPlugin,
    ToggleTags,
    NotebookCellTrackerPlugin
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
/**
 * Activate the notebook widget factory.
 */
function activateDataflowWidgetFactory(app, contentFactory, editorServices, rendermime, toolbarRegistry, settingRegistry, sessionContextDialogs_, translator_) {
    const translator = translator_ !== null && translator_ !== void 0 ? translator_ : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.nullTranslator;
    const sessionContextDialogs = sessionContextDialogs_ !== null && sessionContextDialogs_ !== void 0 ? sessionContextDialogs_ : new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SessionContextDialogs({ translator });
    const preferKernelOption = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_21__.PageConfig.getOption('notebookStartsKernel');
    // If the option is not set, assume `true`
    const preferKernelValue = preferKernelOption === '' || preferKernelOption.toLowerCase() === 'true';
    const { commands } = app;
    let toolbarFactory;
    // Register notebook toolbar widgets
    toolbarRegistry.addFactory(DATAFLOW_FACTORY, 'save', panel => _jupyterlab_docmanager_extension__WEBPACK_IMPORTED_MODULE_6__.ToolbarItems.createSaveButton(commands, panel.context.fileChanged));
    toolbarRegistry.addFactory(DATAFLOW_FACTORY, 'cellType', panel => _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.ToolbarItems.createCellTypeItem(panel, translator));
    toolbarRegistry.addFactory(DATAFLOW_FACTORY, 'kernelName', panel => _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Toolbar.createKernelNameItem(panel.sessionContext, sessionContextDialogs, translator));
    toolbarRegistry.addFactory(DATAFLOW_FACTORY, 'executionProgress', panel => {
        const loadingSettings = settingRegistry === null || settingRegistry === void 0 ? void 0 : settingRegistry.load(trackerPlugin.id);
        const indicator = _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.ExecutionIndicator.createExecutionIndicatorItem(panel, translator, loadingSettings);
        void (loadingSettings === null || loadingSettings === void 0 ? void 0 : loadingSettings.then(settings => {
            panel.disposed.connect(() => {
                settings.dispose();
            });
        }));
        return indicator;
    });
    if (settingRegistry) {
        // Create the factory
        toolbarFactory = (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.createToolbarFactory)(toolbarRegistry, settingRegistry, DATAFLOW_FACTORY, PANEL_SETTINGS, translator);
    }
    const trans = translator.load('jupyterlab');
    const factory = new _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookWidgetFactory({
        name: DATAFLOW_FACTORY,
        label: trans.__('Notebook'),
        fileTypes: ['notebook'],
        modelName: 'dfnotebook',
        defaultFor: ['notebook'],
        preferKernel: preferKernelValue,
        canStartKernel: true,
        rendermime,
        contentFactory,
        editorConfig: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.StaticNotebook.defaultEditorConfig,
        notebookConfig: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.StaticNotebook.defaultNotebookConfig,
        mimeTypeService: editorServices.mimeTypeService,
        toolbarFactory,
        translator
    });
    app.docRegistry.addWidgetFactory(factory);
    return factory;
}
/**
 * Activate the notebook handler extension.
 */
function activateNotebookHandler(app, factory, dfFactory, 
// dfModelFactory: DataflowNotebookModelFactory.IFactory,
extensions, executor, palette, defaultBrowser, launcher, restorer, mainMenu, router, settingRegistry, sessionDialogs_, translator_, formRegistry) {
    (0,_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.setCellExecutor)(executor);
    const translator = translator_ !== null && translator_ !== void 0 ? translator_ : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.nullTranslator;
    const sessionDialogs = sessionDialogs_ !== null && sessionDialogs_ !== void 0 ? sessionDialogs_ : new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SessionContextDialogs({ translator });
    const trans = translator.load('jupyterlab');
    const services = app.serviceManager;
    const { commands, shell } = app;
    const tracker = new _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookTracker({ namespace: 'notebook' });
    // Use the router to deal with hash navigation
    function onRouted(router, location) {
        if (location.hash && tracker.currentWidget) {
            tracker.currentWidget.setFragment(location.hash);
        }
    }
    router === null || router === void 0 ? void 0 : router.routed.connect(onRouted);
    const isEnabled = () => {
        return Private.isEnabled(shell, tracker);
    };
    const setSideBySideOutputRatio = (sideBySideOutputRatio) => document.documentElement.style.setProperty('--jp-side-by-side-output-size', `${sideBySideOutputRatio}fr`);
    // Fetch settings if possible.
    const fetchSettings = settingRegistry
        ? settingRegistry.load(trackerPlugin.id)
        : Promise.reject(new Error(`No setting registry for ${trackerPlugin.id}`));
    fetchSettings
        .then(settings => {
        updateConfig(factory, settings);
        updateConfig(dfFactory, settings);
        settings.changed.connect(() => {
            updateConfig(factory, settings);
            updateConfig(dfFactory, settings);
        });
        const updateSessionSettings = (session, changes) => {
            const { newValue, oldValue } = changes;
            const autoStartDefault = newValue.autoStartDefault;
            if (typeof autoStartDefault === 'boolean' &&
                autoStartDefault !== oldValue.autoStartDefault) {
                // Ensure we break the cycle
                if (autoStartDefault !==
                    settings.get('autoStartDefaultKernel').composite)
                    // Once the settings is changed `updateConfig` will take care
                    // of the propagation to existing session context.
                    settings
                        .set('autoStartDefaultKernel', autoStartDefault)
                        .catch(reason => {
                        console.error(`Failed to set ${settings.id}.autoStartDefaultKernel`);
                    });
            }
        };
        const sessionContexts = new WeakSet();
        const listenToKernelPreference = (panel) => {
            const session = panel.context.sessionContext;
            if (!session.isDisposed && !sessionContexts.has(session)) {
                sessionContexts.add(session);
                session.kernelPreferenceChanged.connect(updateSessionSettings);
                session.disposed.connect(() => {
                    session.kernelPreferenceChanged.disconnect(updateSessionSettings);
                });
            }
        };
        tracker.forEach(listenToKernelPreference);
        tracker.widgetAdded.connect((tracker, panel) => {
            listenToKernelPreference(panel);
        });
        commands.addCommand(CommandIDs.autoClosingBrackets, {
            execute: args => {
                var _a;
                const codeConfig = settings.get('codeCellConfig')
                    .composite;
                const markdownConfig = settings.get('markdownCellConfig')
                    .composite;
                const rawConfig = settings.get('rawCellConfig')
                    .composite;
                const anyToggled = codeConfig.autoClosingBrackets ||
                    markdownConfig.autoClosingBrackets ||
                    rawConfig.autoClosingBrackets;
                const toggled = !!((_a = args['force']) !== null && _a !== void 0 ? _a : !anyToggled);
                [
                    codeConfig.autoClosingBrackets,
                    markdownConfig.autoClosingBrackets,
                    rawConfig.autoClosingBrackets
                ] = [toggled, toggled, toggled];
                void settings.set('codeCellConfig', codeConfig);
                void settings.set('markdownCellConfig', markdownConfig);
                void settings.set('rawCellConfig', rawConfig);
            },
            label: trans.__('Auto Close Brackets for All Notebook Cell Types'),
            isToggled: () => ['codeCellConfig', 'markdownCellConfig', 'rawCellConfig'].some(x => {
                var _a;
                return ((_a = settings.get(x).composite.autoClosingBrackets) !== null && _a !== void 0 ? _a : extensions.baseConfiguration['autoClosingBrackets']) === true;
            })
        });
        commands.addCommand(CommandIDs.setSideBySideRatio, {
            label: trans.__('Set side-by-side ratio'),
            execute: args => {
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getNumber({
                    title: trans.__('Width of the output in side-by-side mode'),
                    value: settings.get('sideBySideOutputRatio').composite
                })
                    .then(result => {
                    setSideBySideOutputRatio(result.value);
                    if (result.value) {
                        void settings.set('sideBySideOutputRatio', result.value);
                    }
                })
                    .catch(console.error);
            }
        });
    })
        .catch((reason) => {
        console.warn(reason.message);
        updateTracker({
            editorConfig: factory.editorConfig,
            notebookConfig: factory.notebookConfig,
            kernelShutdown: factory.shutdownOnClose,
            autoStartDefault: factory.autoStartDefault
        });
    });
    if (formRegistry) {
        const CMRenderer = formRegistry.getRenderer('@jupyterlab/codemirror-extension:plugin.defaultConfig');
        if (CMRenderer) {
            formRegistry.addRenderer('@jupyterlab/notebook-extension:tracker.codeCellConfig', CMRenderer);
            formRegistry.addRenderer('@jupyterlab/notebook-extension:tracker.markdownCellConfig', CMRenderer);
            formRegistry.addRenderer('@jupyterlab/notebook-extension:tracker.rawCellConfig', CMRenderer);
        }
    }
    // Handle state restoration.
    // !!! BEGIN DATAFLOW NOTEBOOK CHANGE !!!
    if (restorer) {
        // FIXME: This needs to get the kernel information from somewhere
        // Unsure that using model will work here...
        // (factory as NotebookWidgetFactory).kernel = "dfpython3";
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: panel => ({
                path: panel.context.path,
                factory: panel.context.model instanceof _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_19__.DataflowNotebookModel
                    ? DATAFLOW_FACTORY
                    : FACTORY
            }),
            // use notebook or dfnotebook prefix on name here...
            name: panel => panel.context.path,
            when: services.ready
        });
    }
    // !!! END DATAFLOW NOTEBOOK CHANGE !!!
    const registry = app.docRegistry;
    const modelFactory = new _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookModelFactory({
        disableDocumentWideUndoRedo: factory.notebookConfig.disableDocumentWideUndoRedo,
        collaborative: true
    });
    registry.addModelFactory(modelFactory);
    // !!! BEGIN DATAFLOW NOTEBOOK CHANGE !!!
    const dfModelFactory = new _dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_19__.DataflowNotebookModelFactory({
        disableDocumentWideUndoRedo: factory.notebookConfig.disableDocumentWideUndoRedo,
        collaborative: true
    });
    registry.addModelFactory(dfModelFactory);
    // !!! END DATAFLOW NOTEBOOK CHANGE !!!
    addCommands(app, tracker, translator, sessionDialogs, isEnabled);
    if (palette) {
        populatePalette(palette, translator);
    }
    let id = 0; // The ID counter for notebook panels.
    const ft = app.docRegistry.getFileType('notebook');
    // !!! DATAFLOW NOTEBOOK CHANGE !!!
    // Make this a function that can be called by both...
    function connectWidgetCreated(factory) {
        factory.widgetCreated.connect((sender, widget) => {
            var _a, _b;
            // If the notebook panel does not have an ID, assign it one.
            widget.id = widget.id || `notebook-${++id}`;
            // Set up the title icon
            widget.title.icon = ft === null || ft === void 0 ? void 0 : ft.icon;
            widget.title.iconClass = (_a = ft === null || ft === void 0 ? void 0 : ft.iconClass) !== null && _a !== void 0 ? _a : '';
            widget.title.iconLabel = (_b = ft === null || ft === void 0 ? void 0 : ft.iconLabel) !== null && _b !== void 0 ? _b : '';
            // Notify the widget tracker if restore data needs to update.
            widget.context.pathChanged.connect(() => {
                void tracker.save(widget);
            });
            // Add the notebook panel to the tracker.
            void tracker.add(widget);
        });
    }
    connectWidgetCreated(factory);
    connectWidgetCreated(dfFactory);
    // !!! END DATAFLOW NOTEBOOK CHANGE !!!
    /**
     * Update the settings of the current tracker.
     */
    function updateTracker(options) {
        tracker.forEach(widget => {
            widget.setConfig(options);
        });
    }
    /**
     * Update the setting values.
     */
    // !!! DATAFLOW NOTEOBOK UPDATE TO PASS FACTORY IN HERE !!!
    function updateConfig(factory, settings) {
        const code = {
            ..._jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.StaticNotebook.defaultEditorConfig.code,
            ...settings.get('codeCellConfig').composite
        };
        const markdown = {
            ..._jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.StaticNotebook.defaultEditorConfig.markdown,
            ...settings.get('markdownCellConfig').composite
        };
        const raw = {
            ..._jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.StaticNotebook.defaultEditorConfig.raw,
            ...settings.get('rawCellConfig').composite
        };
        factory.editorConfig = { code, markdown, raw };
        factory.notebookConfig = {
            enableKernelInitNotification: settings.get('enableKernelInitNotification')
                .composite,
            showHiddenCellsButton: settings.get('showHiddenCellsButton')
                .composite,
            scrollPastEnd: settings.get('scrollPastEnd').composite,
            defaultCell: settings.get('defaultCell').composite,
            recordTiming: settings.get('recordTiming').composite,
            overscanCount: settings.get('overscanCount').composite,
            inputHistoryScope: settings.get('inputHistoryScope').composite,
            maxNumberOutputs: settings.get('maxNumberOutputs').composite,
            showEditorForReadOnlyMarkdown: settings.get('showEditorForReadOnlyMarkdown').composite,
            disableDocumentWideUndoRedo: !settings.get('documentWideUndoRedo')
                .composite,
            renderingLayout: settings.get('renderingLayout').composite,
            sideBySideLeftMarginOverride: settings.get('sideBySideLeftMarginOverride')
                .composite,
            sideBySideRightMarginOverride: settings.get('sideBySideRightMarginOverride').composite,
            sideBySideOutputRatio: settings.get('sideBySideOutputRatio')
                .composite,
            windowingMode: settings.get('windowingMode').composite
        };
        setSideBySideOutputRatio(factory.notebookConfig.sideBySideOutputRatio);
        const sideBySideMarginStyle = `.jp-mod-sideBySide.jp-Notebook .jp-Notebook-cell {
      margin-left: ${factory.notebookConfig.sideBySideLeftMarginOverride} !important;
      margin-right: ${factory.notebookConfig.sideBySideRightMarginOverride} !important;`;
        const sideBySideMarginTag = document.getElementById(SIDE_BY_SIDE_STYLE_ID);
        if (sideBySideMarginTag) {
            sideBySideMarginTag.innerText = sideBySideMarginStyle;
        }
        else {
            document.head.insertAdjacentHTML('beforeend', `<style id="${SIDE_BY_SIDE_STYLE_ID}">${sideBySideMarginStyle}}</style>`);
        }
        factory.autoStartDefault = settings.get('autoStartDefaultKernel')
            .composite;
        factory.shutdownOnClose = settings.get('kernelShutdown')
            .composite;
        modelFactory.disableDocumentWideUndoRedo = !settings.get('documentWideUndoRedo').composite;
        // !!! BEGIN DATAFLOW NOTEBOOK CHANGE !!!
        dfModelFactory.disableDocumentWideUndoRedo = !settings.get('documentWideUndoRedo').composite;
        // !!! END DATAFLOW NOTEBOOK CHANGE !!!
        updateTracker({
            editorConfig: factory.editorConfig,
            notebookConfig: factory.notebookConfig,
            kernelShutdown: factory.shutdownOnClose,
            autoStartDefault: factory.autoStartDefault
        });
    }
    // Add main menu notebook menu.
    if (mainMenu) {
        populateMenus(mainMenu, isEnabled);
    }
    // Utility function to create a new notebook.
    const createNew = async (cwd, kernelId, kernelName) => {
        const model = await commands.execute('docmanager:new-untitled', {
            path: cwd,
            type: 'notebook'
        });
        if (model !== undefined) {
            const widget = (await commands.execute('docmanager:open', {
                path: model.path,
                // !!! DATAFLOW NOTEBOOK CHANGE (ONE LINE) !!!
                factory: kernelName == 'dfpython3' ? DATAFLOW_FACTORY : FACTORY,
                kernel: { id: kernelId, name: kernelName }
            }));
            widget.isUntitled = true;
            return widget;
        }
    };
    // Add a command for creating a new notebook.
    commands.addCommand(CommandIDs.createNew, {
        label: args => {
            var _a, _b, _c;
            const kernelName = args['kernelName'] || '';
            if (args['isLauncher'] && args['kernelName'] && services.kernelspecs) {
                return ((_c = (_b = (_a = services.kernelspecs.specs) === null || _a === void 0 ? void 0 : _a.kernelspecs[kernelName]) === null || _b === void 0 ? void 0 : _b.display_name) !== null && _c !== void 0 ? _c : '');
            }
            if (args['isPalette'] || args['isContextMenu']) {
                return trans.__('New Notebook');
            }
            return trans.__('Notebook');
        },
        caption: trans.__('Create a new notebook'),
        icon: args => (args['isPalette'] ? undefined : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.notebookIcon),
        execute: args => {
            var _a;
            const cwd = args['cwd'] || ((_a = defaultBrowser === null || defaultBrowser === void 0 ? void 0 : defaultBrowser.model.path) !== null && _a !== void 0 ? _a : '');
            const kernelId = args['kernelId'] || '';
            const kernelName = args['kernelName'] || '';
            return createNew(cwd, kernelId, kernelName);
        }
    });
    // Add a launcher item if the launcher is available.
    if (launcher) {
        void services.ready.then(() => {
            let disposables = null;
            const onSpecsChanged = () => {
                if (disposables) {
                    disposables.dispose();
                    disposables = null;
                }
                const specs = services.kernelspecs.specs;
                if (!specs) {
                    return;
                }
                disposables = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_17__.DisposableSet();
                for (const name in specs.kernelspecs) {
                    const rank = name === specs.default ? 0 : Infinity;
                    const spec = specs.kernelspecs[name];
                    const kernelIconUrl = spec.resources['logo-svg'] || spec.resources['logo-64x64'];
                    disposables.add(launcher.add({
                        command: CommandIDs.createNew,
                        args: { isLauncher: true, kernelName: name },
                        category: trans.__('Notebook'),
                        rank,
                        kernelIconUrl,
                        metadata: {
                            kernel: _lumino_coreutils__WEBPACK_IMPORTED_MODULE_16__.JSONExt.deepCopy(spec.metadata || {})
                        }
                    }));
                }
            };
            onSpecsChanged();
            services.kernelspecs.specsChanged.connect(onSpecsChanged);
        });
    }
    return tracker;
}
// Get the current widget and activate unless the args specify otherwise.
function getCurrent(tracker, shell, args) {
    const widget = tracker.currentWidget;
    const activate = args['activate'] !== false;
    if (activate && widget) {
        shell.activateById(widget.id);
    }
    return widget;
}
/**
 * Add the notebook commands to the application's command registry.
 */
function addCommands(app, tracker, translator, sessionDialogs, isEnabled) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    const isEnabledAndSingleSelected = () => {
        return Private.isEnabledAndSingleSelected(shell, tracker);
    };
    const refreshCellCollapsed = (notebook) => {
        var _a, _b;
        for (const cell of notebook.widgets) {
            if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.MarkdownCell && cell.headingCollapsed) {
                _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.setHeadingCollapse(cell, true, notebook);
            }
            if (cell.model.id === ((_b = (_a = notebook.activeCell) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.id)) {
                _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.expandParent(cell, notebook);
            }
        }
    };
    const isEnabledAndHeadingSelected = () => {
        return Private.isEnabledAndHeadingSelected(shell, tracker);
    };
    // Set up signal handler to keep the collapse state consistent
    tracker.currentChanged.connect((sender, panel) => {
        var _a, _b;
        if (!((_b = (_a = panel === null || panel === void 0 ? void 0 : panel.content) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.cells)) {
            return;
        }
        panel.content.model.cells.changed.connect((list, args) => {
            // Might be overkill to refresh this every time, but
            // it helps to keep the collapse state consistent.
            refreshCellCollapsed(panel.content);
        });
        panel.content.activeCellChanged.connect((notebook, cell) => {
            _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.expandParent(cell, notebook);
        });
    });
    tracker.selectionChanged.connect(() => {
        commands.notifyCommandChanged(CommandIDs.duplicateBelow);
        commands.notifyCommandChanged(CommandIDs.deleteCell);
        commands.notifyCommandChanged(CommandIDs.copy);
        commands.notifyCommandChanged(CommandIDs.cut);
        commands.notifyCommandChanged(CommandIDs.pasteBelow);
        commands.notifyCommandChanged(CommandIDs.pasteAbove);
        commands.notifyCommandChanged(CommandIDs.pasteAndReplace);
        commands.notifyCommandChanged(CommandIDs.moveUp);
        commands.notifyCommandChanged(CommandIDs.moveDown);
        commands.notifyCommandChanged(CommandIDs.run);
        commands.notifyCommandChanged(CommandIDs.runAll);
        commands.notifyCommandChanged(CommandIDs.runAndAdvance);
        commands.notifyCommandChanged(CommandIDs.runAndInsert);
    });
    tracker.activeCellChanged.connect(() => {
        commands.notifyCommandChanged(CommandIDs.moveUp);
        commands.notifyCommandChanged(CommandIDs.moveDown);
        commands.notifyCommandChanged(CommandIDs.tagCodeCell);
    });
    commands.addCommand(CommandIDs.runAndAdvance, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Run Selected Cell', 'Run Selected Cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Run this cell and advance', 'Run these %1 cells and advance', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.runAndAdvance(content, context.sessionContext, sessionDialogs, translator);
            }
        },
        isEnabled: args => (args.toolbar ? true : isEnabled()),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.runIcon : undefined)
    });
    commands.addCommand(CommandIDs.run, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Run Selected Cell and Do not Advance', 'Run Selected Cells and Do not Advance', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.run(content, context.sessionContext, sessionDialogs, translator);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runAndInsert, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Run Selected Cell and Insert Below', 'Run Selected Cells and Insert Below', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.runAndInsert(content, context.sessionContext, sessionDialogs, translator);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runAll, {
        label: trans.__('Run All Cells'),
        caption: trans.__('Run all cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.runAll(content, context.sessionContext, sessionDialogs, translator);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runAllAbove, {
        label: trans.__('Run All Above Selected Cell'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.runAllAbove(content, context.sessionContext, sessionDialogs, translator);
            }
        },
        isEnabled: () => {
            // Can't run above if there are multiple cells selected,
            // or if we are at the top of the notebook.
            return (isEnabledAndSingleSelected() &&
                tracker.currentWidget.content.activeCellIndex !== 0);
        }
    });
    commands.addCommand(CommandIDs.runAllBelow, {
        label: trans.__('Run Selected Cell and All Below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.runAllBelow(content, context.sessionContext, sessionDialogs, translator);
            }
        },
        isEnabled: () => {
            // Can't run below if there are multiple cells selected,
            // or if we are at the bottom of the notebook.
            return (isEnabledAndSingleSelected() &&
                tracker.currentWidget.content.activeCellIndex !==
                    tracker.currentWidget.content.widgets.length - 1);
        }
    });
    commands.addCommand(CommandIDs.renderAllMarkdown, {
        label: trans.__('Render All Markdown Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { content } = current;
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.renderAllMarkdown(content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.restart, {
        label: trans.__('Restart Kernel…'),
        caption: trans.__('Restart the kernel'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return sessionDialogs.restart(current.sessionContext);
            }
        },
        isEnabled: args => (args.toolbar ? true : isEnabled()),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.refreshIcon : undefined)
    });
    commands.addCommand(CommandIDs.shutdown, {
        label: trans.__('Shut Down Kernel'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (!current) {
                return;
            }
            return current.context.sessionContext.shutdown();
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.closeAndShutdown, {
        label: trans.__('Close and Shut Down Notebook'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (!current) {
                return;
            }
            const fileName = current.title.label;
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Shut down the notebook?'),
                body: trans.__('Are you sure you want to close "%1"?', fileName),
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton()]
            }).then(result => {
                if (result.button.accept) {
                    return commands
                        .execute(CommandIDs.shutdown, { activate: false })
                        .then(() => {
                        current.dispose();
                    });
                }
            });
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.trust, {
        label: () => trans.__('Trust Notebook'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.trust(content).then(() => context.save());
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.restartClear, {
        label: trans.__('Restart Kernel and Clear Outputs of All Cells…'),
        caption: trans.__('Restart the kernel and clear all outputs of all cells'),
        execute: async () => {
            const restarted = await commands.execute(CommandIDs.restart, {
                activate: false
            });
            if (restarted) {
                await commands.execute(CommandIDs.clearAllOutputs);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.restartAndRunToSelected, {
        label: trans.__('Restart Kernel and Run up to Selected Cell…'),
        execute: async () => {
            const restarted = await commands.execute(CommandIDs.restart, {
                activate: false
            });
            if (restarted) {
                const executed = await commands.execute(CommandIDs.runAllAbove, { activate: false });
                if (executed) {
                    return commands.execute(CommandIDs.run);
                }
            }
        },
        isEnabled: isEnabledAndSingleSelected
    });
    commands.addCommand(CommandIDs.restartRunAll, {
        label: trans.__('Restart Kernel and Run All Cells…'),
        caption: trans.__('Restart the kernel and run all cells'),
        execute: async () => {
            const restarted = await commands.execute(CommandIDs.restart, {
                activate: false
            });
            if (restarted) {
                await commands.execute(CommandIDs.runAll);
            }
        },
        isEnabled: args => (args.toolbar ? true : isEnabled()),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.fastForwardIcon : undefined)
    });
    commands.addCommand(CommandIDs.clearAllOutputs, {
        label: trans.__('Clear Outputs of All Cells'),
        caption: trans.__('Clear all outputs of all cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.clearAllOutputs(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.clearOutputs, {
        label: trans.__('Clear Cell Output'),
        caption: trans.__('Clear outputs for the selected cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.clearOutputs(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.interrupt, {
        label: trans.__('Interrupt Kernel'),
        caption: trans.__('Interrupt the kernel'),
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (!current) {
                return;
            }
            const kernel = (_a = current.context.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (kernel) {
                return kernel.interrupt();
            }
        },
        isEnabled: args => (args.toolbar ? true : isEnabled()),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.stopIcon : undefined)
    });
    commands.addCommand(CommandIDs.toCode, {
        label: trans.__('Change to Code Cell Type'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.changeCellType(current.content, 'code');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.toMarkdown, {
        label: trans.__('Change to Markdown Cell Type'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.changeCellType(current.content, 'markdown');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.toRaw, {
        label: trans.__('Change to Raw Cell Type'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.changeCellType(current.content, 'raw');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.cut, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Cut Cell', 'Cut Cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Cut this cell', 'Cut these %1 cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.cut(current.content);
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.cutIcon : undefined),
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.copy, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Copy Cell', 'Copy Cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Copy this cell', 'Copy these %1 cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.copy(current.content);
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.copyIcon : undefined),
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.pasteBelow, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Paste Cell Below', 'Paste Cells Below', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Paste this cell from the clipboard', 'Paste these %1 cells from the clipboard', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.paste(current.content, 'below');
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.pasteIcon : undefined),
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.pasteAbove, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Paste Cell Above', 'Paste Cells Above', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Paste this cell from the clipboard', 'Paste these %1 cells from the clipboard', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.paste(current.content, 'above');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.duplicateBelow, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Duplicate Cell Below', 'Duplicate Cells Below', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Create a duplicate of this cell below', 'Create duplicates of %1 cells below', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.duplicate(current.content, 'belowSelected');
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.duplicateIcon : undefined),
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.pasteAndReplace, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Paste Cell and Replace', 'Paste Cells and Replace', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.paste(current.content, 'replace');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.deleteCell, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Delete Cell', 'Delete Cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Delete this cell', 'Delete these %1 cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.deleteCells(current.content);
            }
        },
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.split, {
        label: trans.__('Split Cell'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.splitCell(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.merge, {
        label: trans.__('Merge Selected Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.mergeCells(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.mergeAbove, {
        label: trans.__('Merge Cell Above'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.mergeCells(current.content, true);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.mergeBelow, {
        label: trans.__('Merge Cell Below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.mergeCells(current.content, false);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.insertAbove, {
        label: trans.__('Insert Cell Above'),
        caption: trans.__('Insert a cell above'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.insertAbove(current.content);
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.addAboveIcon : undefined),
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.insertBelow, {
        label: trans.__('Insert Cell Below'),
        caption: trans.__('Insert a cell below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.insertBelow(current.content);
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.addBelowIcon : undefined),
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.selectAbove, {
        label: trans.__('Select Cell Above'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.selectAbove(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.selectBelow, {
        label: trans.__('Select Cell Below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.selectBelow(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.insertHeadingAbove, {
        label: trans.__('Insert Heading Above Current Heading'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.insertSameLevelHeadingAbove(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.insertHeadingBelow, {
        label: trans.__('Insert Heading Below Current Heading'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.insertSameLevelHeadingBelow(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.selectHeadingAboveOrCollapse, {
        label: trans.__('Select Heading Above or Collapse Heading'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.selectHeadingAboveOrCollapseHeading(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.selectHeadingBelowOrExpand, {
        label: trans.__('Select Heading Below or Expand Heading'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.selectHeadingBelowOrExpandHeading(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.extendAbove, {
        label: trans.__('Extend Selection Above'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.extendSelectionAbove(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.extendTop, {
        label: trans.__('Extend Selection to Top'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.extendSelectionAbove(current.content, true);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.extendBelow, {
        label: trans.__('Extend Selection Below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.extendSelectionBelow(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.extendBottom, {
        label: trans.__('Extend Selection to Bottom'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.extendSelectionBelow(current.content, true);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.selectAll, {
        label: trans.__('Select All Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.selectAll(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.deselectAll, {
        label: trans.__('Deselect All Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.deselectAll(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.moveUp, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Move Cell Up', 'Move Cells Up', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Move this cell up', 'Move these %1 cells up', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.moveUp(current.content);
                Private.raiseSilentNotification(trans.__('Notebook cell shifted up successfully'), current.node);
            }
        },
        isEnabled: args => {
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            if (!current) {
                return false;
            }
            return current.content.activeCellIndex >= 1;
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.moveUpIcon : undefined)
    });
    commands.addCommand(CommandIDs.moveDown, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Move Cell Down', 'Move Cells Down', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Move this cell down', 'Move these %1 cells down', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.moveDown(current.content);
                Private.raiseSilentNotification(trans.__('Notebook cell shifted down successfully'), current.node);
            }
        },
        isEnabled: args => {
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            if (!current || !current.content.model) {
                return false;
            }
            const length = current.content.model.cells.length;
            return current.content.activeCellIndex < length - 1;
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.moveDownIcon : undefined)
    });
    commands.addCommand(CommandIDs.toggleAllLines, {
        label: trans.__('Show Line Numbers'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.toggleAllLineNumbers(current.content);
            }
        },
        isEnabled,
        isToggled: args => {
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            if (current) {
                const config = current.content.editorConfig;
                return !!(config.code.lineNumbers &&
                    config.markdown.lineNumbers &&
                    config.raw.lineNumbers);
            }
            else {
                return false;
            }
        }
    });
    commands.addCommand(CommandIDs.commandMode, {
        label: trans.__('Enter Command Mode'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                current.content.mode = 'command';
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.editMode, {
        label: trans.__('Enter Edit Mode'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                current.content.mode = 'edit';
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.undoCellAction, {
        label: trans.__('Undo Cell Operation'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.undo(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.redoCellAction, {
        label: trans.__('Redo Cell Operation'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.redo(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.redo, {
        label: trans.__('Redo'),
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const cell = current.content.activeCell;
                if (cell) {
                    cell.inputHidden = false;
                    return (_a = cell.editor) === null || _a === void 0 ? void 0 : _a.redo();
                }
            }
        }
    });
    commands.addCommand(CommandIDs.undo, {
        label: trans.__('Undo'),
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const cell = current.content.activeCell;
                if (cell) {
                    cell.inputHidden = false;
                    return (_a = cell.editor) === null || _a === void 0 ? void 0 : _a.undo();
                }
            }
        }
    });
    commands.addCommand(CommandIDs.changeKernel, {
        label: trans.__('Change Kernel…'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return sessionDialogs.selectKernel(current.context.sessionContext);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.getKernel, {
        label: trans.__('Get Kernel'),
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, { activate: false, ...args });
            if (current) {
                return (_a = current.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.reconnectToKernel, {
        label: trans.__('Reconnect to Kernel'),
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (!current) {
                return;
            }
            const kernel = (_a = current.context.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (kernel) {
                return kernel.reconnect();
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown1, {
        label: trans.__('Change to Heading 1'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.setMarkdownHeader(current.content, 1);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown2, {
        label: trans.__('Change to Heading 2'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.setMarkdownHeader(current.content, 2);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown3, {
        label: trans.__('Change to Heading 3'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.setMarkdownHeader(current.content, 3);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown4, {
        label: trans.__('Change to Heading 4'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.setMarkdownHeader(current.content, 4);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown5, {
        label: trans.__('Change to Heading 5'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.setMarkdownHeader(current.content, 5);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown6, {
        label: trans.__('Change to Heading 6'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.setMarkdownHeader(current.content, 6);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.hideCode, {
        label: trans.__('Collapse Selected Code'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.hideCode(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.showCode, {
        label: trans.__('Expand Selected Code'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.showCode(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.hideAllCode, {
        label: trans.__('Collapse All Code'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.hideAllCode(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.showAllCode, {
        label: trans.__('Expand All Code'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.showAllCode(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.hideOutput, {
        label: trans.__('Collapse Selected Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.hideOutput(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.showOutput, {
        label: trans.__('Expand Selected Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.showOutput(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.hideAllOutputs, {
        label: trans.__('Collapse All Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.hideAllOutputs(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.toggleRenderSideBySideCurrentNotebook, {
        label: trans.__('Render Side-by-Side'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                if (current.content.renderingLayout === 'side-by-side') {
                    return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.renderDefault(current.content);
                }
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.renderSideBySide(current.content);
            }
        },
        isEnabled,
        isToggled: args => {
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            if (current) {
                return current.content.renderingLayout === 'side-by-side';
            }
            else {
                return false;
            }
        }
    });
    commands.addCommand(CommandIDs.showAllOutputs, {
        label: trans.__('Expand All Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.showAllOutputs(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.enableOutputScrolling, {
        label: trans.__('Enable Scrolling for Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.enableOutputScrolling(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.disableOutputScrolling, {
        label: trans.__('Disable Scrolling for Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.disableOutputScrolling(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.selectLastRunCell, {
        label: trans.__('Select current running or last run cell'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.selectLastRunCell(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.replaceSelection, {
        label: trans.__('Replace Selection in Notebook Cell'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            const text = args['text'] || '';
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.replaceSelection(current.content, text);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.toggleCollapseCmd, {
        label: trans.__('Toggle Collapse Notebook Heading'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.toggleCurrentHeadingCollapse(current.content);
            }
        },
        isEnabled: isEnabledAndHeadingSelected
    });
    commands.addCommand(CommandIDs.collapseAllCmd, {
        label: trans.__('Collapse All Headings'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.collapseAllHeadings(current.content);
            }
        }
    });
    commands.addCommand(CommandIDs.expandAllCmd, {
        label: trans.__('Expand All Headings'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.expandAllHeadings(current.content);
            }
        }
    });
    commands.addCommand(CommandIDs.tocRunCells, {
        label: trans.__('Select and Run Cell(s) for this Heading'),
        execute: args => {
            const current = getCurrent(tracker, shell, { activate: false, ...args });
            if (current === null) {
                return;
            }
            const activeCell = current.content.activeCell;
            let lastIndex = current.content.activeCellIndex;
            if (activeCell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.MarkdownCell) {
                const cells = current.content.widgets;
                const level = activeCell.headingInfo.level;
                for (let i = current.content.activeCellIndex + 1; i < cells.length; i++) {
                    const cell = cells[i];
                    if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.MarkdownCell &&
                        // cell.headingInfo.level === -1 if no heading
                        cell.headingInfo.level >= 0 &&
                        cell.headingInfo.level <= level) {
                        break;
                    }
                    lastIndex = i;
                }
            }
            current.content.extendContiguousSelectionTo(lastIndex);
            _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.NotebookActions.run(current.content, current.sessionContext, sessionDialogs, translator);
        }
    });
    commands.addCommand(CommandIDs.addCellTag, {
        label: 'Add Cell Tag',
        execute: async (args) => {
            var _a, _b, _c, _d;
            const cell = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.activeCell;
            if (cell == null) {
                return;
            }
            const existingCellTags = new Set();
            let cells = (_c = (_b = tracker.currentWidget) === null || _b === void 0 ? void 0 : _b.content.model) === null || _c === void 0 ? void 0 : _c.cells;
            if (cells) {
                for (let index = 0; index < cells.length; index++) {
                    let cAny = cells.get(index);
                    if (cAny.type == 'code') {
                        const dfmetadata = cAny.getMetadata('dfmetadata');
                        const cellTagvalue = dfmetadata.tag;
                        if (cellTagvalue) {
                            existingCellTags.add(cellTagvalue);
                        }
                    }
                }
            }
            const inputArea = cell.inputArea;
            const hexRegexp = new RegExp('^[0-9a-f]{8}$');
            const pythonVarRegexp = new RegExp('^[a-zA-Z0-9_]*$');
            // Function to create the dialog node
            const createTagNode = (oldTag, errorMessage = '') => {
                const body = document.createElement('div');
                const input = document.createElement('input');
                input.name = 'tag-name';
                input.placeholder = 'Enter tag name';
                input.style.margin = '10px 0 10px 0';
                const message = document.createElement('div');
                message.style.color = 'red';
                message.style.marginTop = '10px';
                message.id = 'error-message';
                message.textContent = errorMessage;
                body.appendChild(input);
                body.appendChild(document.createElement('br'));
                body.appendChild(message);
                return body;
            };
            const showAddTagDialog = async (errorMessage = '') => {
                const dialogNode = createTagNode(inputArea.tag, errorMessage);
                const widgetNode = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_18__.Widget();
                widgetNode.node.appendChild(dialogNode);
                const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: 'Add Cell Tag',
                    body: widgetNode,
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Add' })
                    ],
                    focusNodeSelector: 'input[name="tag-name"]',
                });
                if (result.button.accept) {
                    const newTag = dialogNode.querySelector('input[name="tag-name"]').value;
                    if (newTag.trim() === '') {
                        return await showAddTagDialog('Tag cannot be empty or whitespace. Enter a valid tag.');
                    }
                    else if (!pythonVarRegexp.test(newTag)) {
                        return await showAddTagDialog('Invalid name (follow python identifier rules). Enter a valid tag.');
                    }
                    else if (hexRegexp.test(newTag)) {
                        return await showAddTagDialog('Cell tags cannot be 8 hex values. Enter a valid tag.');
                    }
                    else if (existingCellTags.has(newTag)) {
                        return await showAddTagDialog('This tag already exists. Enter a different tag.');
                    }
                    else {
                        return { newTag };
                    }
                }
                return null;
            };
            const result = await showAddTagDialog();
            const cellUUID = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_10__.truncateCellId)(cell.model.id);
            const notebookId = (0,_dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_22__.getNotebookId)(cell);
            if (result) {
                const { newTag } = result;
                inputArea.addTag(newTag);
                if (newTag && ((_d = tracker.currentWidget) === null || _d === void 0 ? void 0 : _d.content.model)) {
                    let notebook = tracker.currentWidget.content.model;
                    await updateNotebookCellsWithTag(notebookId, notebook, cellUUID, tracker.currentWidget.sessionContext);
                }
            }
        },
        isEnabled: () => {
            var _a, _b, _c, _d;
            const cell = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.activeCell;
            const isTagsVisible = (_c = (_b = tracker.currentWidget) === null || _b === void 0 ? void 0 : _b.model) === null || _c === void 0 ? void 0 : _c.getMetadata('enable_tags');
            if (cell && cell.model.type == 'code' && cell.inputArea) {
                const inputArea = cell.inputArea;
                return (((_d = inputArea.tag) === null || _d === void 0 ? void 0 : _d.length) ? false : true) && isTagsVisible;
            }
            return false;
        },
        isVisible: () => {
            var _a, _b;
            const isDfnotebook = (_b = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.getMetadata('dfnotebook');
            return isDfnotebook === true;
        }
    });
    commands.addCommand(CommandIDs.modifyCellTag, {
        label: 'Modify Cell Tag',
        execute: async (args) => {
            var _a, _b, _c, _d, _e;
            const cell = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.activeCell;
            const existingCellTags = new Set();
            let cells = (_c = (_b = tracker.currentWidget) === null || _b === void 0 ? void 0 : _b.content.model) === null || _c === void 0 ? void 0 : _c.cells;
            if (cells) {
                for (let index = 0; index < cells.length; index++) {
                    let cAny = cells.get(index);
                    if (cAny.type == 'code') {
                        const dfmetadata = cAny.getMetadata('dfmetadata');
                        const cellTagvalue = dfmetadata.tag;
                        if (cellTagvalue) {
                            existingCellTags.add(cellTagvalue);
                        }
                    }
                }
            }
            if (cell == null) {
                return;
            }
            const inputArea = cell.inputArea;
            if (!inputArea.tag) {
                alert('This cell does not have a tag.');
                return;
            }
            const hexRegexp = new RegExp('^[0-9a-f]{8}$');
            const pythonVarRegexp = new RegExp('^[a-zA-Z0-9_]*$');
            // Function to create the dialog node
            const createRenameTagNode = (oldTag, errorMessage = '') => {
                const body = document.createElement('div');
                const inputLabel = document.createElement('label');
                inputLabel.textContent = `Current Tag: ${oldTag}`;
                const input = document.createElement('input');
                input.name = 'new-tag';
                input.placeholder = 'Enter new tag';
                input.classList.add('rename-tag-input');
                const updateReferencesLabel = document.createElement('label');
                updateReferencesLabel.textContent = 'Update references';
                updateReferencesLabel.classList.add('update-references-label');
                const updateReferencesCheckbox = document.createElement('input');
                updateReferencesCheckbox.name = 'update-references';
                updateReferencesCheckbox.type = 'checkbox';
                updateReferencesCheckbox.checked = true;
                updateReferencesCheckbox.classList.add('update-references-checkbox');
                const message = document.createElement('div');
                message.id = 'error-message';
                message.textContent = errorMessage;
                message.classList.add('error-message');
                body.appendChild(inputLabel);
                body.appendChild(document.createElement('br'));
                body.appendChild(input);
                body.appendChild(document.createElement('br'));
                body.appendChild(updateReferencesLabel);
                body.appendChild(updateReferencesCheckbox);
                body.appendChild(message);
                return body;
            };
            const showModifyTagDialog = async (errorMessage = '') => {
                const dialogNode = createRenameTagNode(inputArea.tag, errorMessage);
                const widgetNode = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_18__.Widget();
                widgetNode.node.appendChild(dialogNode);
                const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: 'Modify Cell Tag',
                    body: widgetNode,
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Delete' }),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Modify' })
                    ],
                    focusNodeSelector: 'input[name="new-tag"]',
                });
                if (result.button.accept) {
                    const newTag = dialogNode.querySelector('input[name="new-tag"]').value;
                    const updateReferences = dialogNode.querySelector('input[name="update-references"]').checked;
                    const deleteTag = result.button.label === 'Delete';
                    if (deleteTag) {
                        return { newTag: '', updateReferences };
                    }
                    if (newTag.trim() === '') {
                        return await showModifyTagDialog('Tag cannot be empty or whitespace. Enter a valid tag.');
                    }
                    else if (!pythonVarRegexp.test(newTag)) {
                        return await showModifyTagDialog('Invalid name (follow python identifier rules). Enter a valid tag.');
                    }
                    else if (hexRegexp.test(newTag)) {
                        return await showModifyTagDialog('Cell tags cannot be 8 hex values. Enter a valid tag.');
                    }
                    else if (existingCellTags.has(newTag)) {
                        return await showModifyTagDialog('This tag already exists. Enter a different tag.');
                    }
                    else {
                        return { newTag, updateReferences };
                    }
                }
                return null;
            };
            const result = await showModifyTagDialog();
            const cellUUID = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_10__.truncateCellId)(cell.model.id);
            const notebookId = (0,_dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_22__.getNotebookId)(cell);
            if (result) {
                const { newTag, updateReferences } = result;
                inputArea.addTag(newTag);
                if (updateReferences && ((_d = tracker.currentWidget) === null || _d === void 0 ? void 0 : _d.content.model)) {
                    let notebook = tracker.currentWidget.content.model;
                    await updateNotebookCellsWithTag(notebookId, notebook, cellUUID, tracker.currentWidget.sessionContext);
                }
                else if (updateReferences == false && ((_e = tracker.currentWidget) === null || _e === void 0 ? void 0 : _e.content.model)) {
                    let notebook = tracker.currentWidget.content.model;
                    const all_tags = {};
                    for (let index = 0; index < notebook.cells.length; index++) {
                        const cAny = notebook.cells.get(index);
                        if (notebook.cells.get(index).type === 'code') {
                            const c = cAny;
                            const cId = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_10__.truncateCellId)(c.id);
                            const dfmetadata = c.getMetadata('dfmetadata');
                            if (dfmetadata.tag) {
                                all_tags[cId] = dfmetadata.tag;
                            }
                        }
                    }
                    for (let index = 0; index < notebook.cells.length; index++) {
                        const cAny = notebook.cells.get(index);
                        if (cAny.type == 'code') {
                            const dfmetadata = notebook.cells.get(index).getMetadata('dfmetadata');
                            let inputVarsMetadata = dfmetadata.inputVars;
                            if (inputVarsMetadata && typeof inputVarsMetadata === 'object' && 'ref' in inputVarsMetadata) {
                                const refValue = inputVarsMetadata.ref;
                                const tagRefValue = {};
                                for (const ref_key in refValue) {
                                    if (ref_key != cellUUID && all_tags.hasOwnProperty(ref_key)) {
                                        tagRefValue[ref_key] = all_tags[ref_key];
                                    }
                                }
                                dfmetadata.inputVars = { 'ref': refValue, 'tag_refs': tagRefValue };
                                notebook.cells.get(index).setMetadata('dfmetadata', dfmetadata);
                                await updateNotebookCellsWithTag(notebookId, notebook, cellUUID, tracker.currentWidget.sessionContext, false, true);
                            }
                        }
                    }
                }
            }
        },
        isEnabled: () => {
            var _a, _b, _c, _d;
            const cell = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.activeCell;
            const isTagsVisible = (_c = (_b = tracker.currentWidget) === null || _b === void 0 ? void 0 : _b.model) === null || _c === void 0 ? void 0 : _c.getMetadata('enable_tags');
            if (cell && cell.model.type == 'code' && cell.inputArea) {
                const inputArea = cell.inputArea;
                return ((_d = inputArea.tag) === null || _d === void 0 ? void 0 : _d.length) && isTagsVisible;
            }
            return false;
        },
        isVisible: () => {
            var _a, _b;
            const isDfnotebook = (_b = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.getMetadata('dfnotebook');
            return isDfnotebook === true;
        }
    });
    commands.addCommand(CommandIDs.tagCodeCell, {
        label: trans.__('Tag'),
        caption: trans.__('Tag'),
        execute: args => {
            var _a;
            const cell = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.activeCell;
            const inputArea = cell.inputArea;
            if (cell && inputArea && inputArea.tag) {
                commands.execute('notebook:modify-cell-tag');
            }
            else {
                commands.execute('notebook:add-cell-tag');
            }
        },
        isEnabled: () => {
            var _a, _b, _c, _d;
            const isDfnotebook = (_b = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.getMetadata('dfnotebook');
            const isTagsVisible = (_d = (_c = tracker.currentWidget) === null || _c === void 0 ? void 0 : _c.model) === null || _d === void 0 ? void 0 : _d.getMetadata('enable_tags');
            return isDfnotebook && isTagsVisible;
        },
        isVisible: () => {
            var _a, _b;
            const isDfnotebook = (_b = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.getMetadata('dfnotebook');
            const activeCell = tracker.activeCell;
            return isDfnotebook && (activeCell === null || activeCell === void 0 ? void 0 : activeCell.model.type) === 'code';
        },
        icon: args => (args.toolbar ? tagIcon : undefined)
    });
    // !!! END DATAFLOW NOTEBOOK CHANGE !!!
}
/**
 * Update code based on add, delete or modified tag value
 */
async function updateNotebookCellsWithTag(notebookId, notebook, cellUUID, sessionContext, hideTags = false, updateInputTagsOnly = false) {
    let dfData = (0,_dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_19__.getCellsMetadata)(notebook, '');
    let cellMap = notebookId ? _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_22__.notebookCellMap.get(notebookId) : new Map();
    if (cellMap) {
        const executedCode = {};
        cellMap.forEach((value, key) => {
            executedCode[key] = value;
        });
        dfData.dfMetadata.executed_code = executedCode;
    }
    if (hideTags) {
        dfData.dfMetadata.input_tags = {};
    }
    if (updateInputTagsOnly) {
        dfData.dfMetadata.all_refs = {};
        dfData.dfMetadata.output_tags = {};
        dfData.dfMetadata.code_dict = {};
    }
    try {
        const response = await (0,_dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_19__.dfCommGetData)(sessionContext, { 'dfMetadata': dfData.dfMetadata, 'updateExecutedCode': true });
        updateNotebookCells(notebookId, notebook, response, cellUUID, hideTags);
    }
    catch (error) {
        console.error('Error occured during kernel communication', error);
    }
}
function updateNotebookCells(notebookId, notebook, content, cellUUID, hideTags) {
    const cellMap = notebookId ? _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_22__.notebookCellMap.get(notebookId) : undefined;
    const all_Tags = (0,_dfnotebook_dfnotebook__WEBPACK_IMPORTED_MODULE_19__.getAllTags)(notebook);
    const cellsArray = Array.from(notebook.cells);
    cellsArray.forEach((cell, index) => {
        var _a, _b;
        if (cell.type === 'code') {
            const cAny = cell;
            const cId = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_10__.truncateCellId)(cAny.id);
            // Handle executed code updates
            if ((_a = content.executed_code_dict) === null || _a === void 0 ? void 0 : _a.hasOwnProperty(cId)) {
                const updatedCode = content.executed_code_dict[cId];
                cellMap === null || cellMap === void 0 ? void 0 : cellMap.set(cId, updatedCode.trim());
            }
            // Handle code dictionary updates
            if ((_b = content.code_dict) === null || _b === void 0 ? void 0 : _b.hasOwnProperty(cId)) {
                const updatedCode = content.code_dict[cId];
                cAny.sharedModel.setSource(updatedCode);
            }
            //Updating the dependent cell's df-metadata when any cell is tagged/untagged
            if (cellUUID && !hideTags) {
                const dfmetadata = cAny.getMetadata('dfmetadata');
                const inputVarsMetadata = dfmetadata.inputVars;
                if (inputVarsMetadata && typeof inputVarsMetadata === 'object' && 'ref' in inputVarsMetadata) {
                    const refValue = inputVarsMetadata.ref;
                    let tagRefValue = inputVarsMetadata.tag_refs;
                    for (const ref_key in refValue) {
                        if (ref_key == cellUUID && all_Tags.hasOwnProperty(ref_key)) {
                            tagRefValue[cellUUID] = all_Tags[cellUUID];
                        }
                    }
                    dfmetadata.inputVars = { 'ref': refValue, 'tag_refs': tagRefValue };
                    notebook.cells.get(index).setMetadata('dfmetadata', dfmetadata);
                }
            }
        }
    });
}
/**
 * Populate the application's command palette with notebook commands.
 */
function populatePalette(palette, translator) {
    const trans = translator.load('jupyterlab');
    let category = trans.__('Notebook Operations');
    [
        CommandIDs.interrupt,
        CommandIDs.restart,
        CommandIDs.restartClear,
        CommandIDs.restartRunAll,
        CommandIDs.runAll,
        CommandIDs.renderAllMarkdown,
        CommandIDs.runAllAbove,
        CommandIDs.runAllBelow,
        CommandIDs.restartAndRunToSelected,
        CommandIDs.selectAll,
        CommandIDs.deselectAll,
        CommandIDs.clearAllOutputs,
        CommandIDs.toggleAllLines,
        CommandIDs.editMode,
        CommandIDs.commandMode,
        CommandIDs.changeKernel,
        CommandIDs.reconnectToKernel,
        CommandIDs.createConsole,
        CommandIDs.closeAndShutdown,
        CommandIDs.trust,
        CommandIDs.toggleCollapseCmd,
        CommandIDs.collapseAllCmd,
        CommandIDs.expandAllCmd
    ].forEach(command => {
        palette.addItem({ command, category });
    });
    palette.addItem({
        command: CommandIDs.createNew,
        category,
        args: { isPalette: true }
    });
    category = trans.__('Notebook Cell Operations');
    [
        CommandIDs.run,
        CommandIDs.runAndAdvance,
        CommandIDs.runAndInsert,
        CommandIDs.runInConsole,
        CommandIDs.clearOutputs,
        CommandIDs.toCode,
        CommandIDs.toMarkdown,
        CommandIDs.toRaw,
        CommandIDs.cut,
        CommandIDs.copy,
        CommandIDs.pasteBelow,
        CommandIDs.pasteAbove,
        CommandIDs.pasteAndReplace,
        CommandIDs.deleteCell,
        CommandIDs.split,
        CommandIDs.merge,
        CommandIDs.mergeAbove,
        CommandIDs.mergeBelow,
        CommandIDs.insertAbove,
        CommandIDs.insertBelow,
        CommandIDs.selectAbove,
        CommandIDs.selectBelow,
        CommandIDs.selectHeadingAboveOrCollapse,
        CommandIDs.selectHeadingBelowOrExpand,
        CommandIDs.insertHeadingAbove,
        CommandIDs.insertHeadingBelow,
        CommandIDs.extendAbove,
        CommandIDs.extendTop,
        CommandIDs.extendBelow,
        CommandIDs.extendBottom,
        CommandIDs.moveDown,
        CommandIDs.moveUp,
        CommandIDs.undoCellAction,
        CommandIDs.redoCellAction,
        CommandIDs.markdown1,
        CommandIDs.markdown2,
        CommandIDs.markdown3,
        CommandIDs.markdown4,
        CommandIDs.markdown5,
        CommandIDs.markdown6,
        CommandIDs.hideCode,
        CommandIDs.showCode,
        CommandIDs.hideAllCode,
        CommandIDs.showAllCode,
        CommandIDs.hideOutput,
        CommandIDs.showOutput,
        CommandIDs.hideAllOutputs,
        CommandIDs.showAllOutputs,
        CommandIDs.toggleRenderSideBySideCurrentNotebook,
        CommandIDs.setSideBySideRatio,
        CommandIDs.enableOutputScrolling,
        CommandIDs.disableOutputScrolling,
        CommandIDs.tagCodeCell
    ].forEach(command => {
        palette.addItem({ command, category });
    });
}
/**
 * Populates the application menus for the notebook.
 */
function populateMenus(mainMenu, isEnabled) {
    // Add undo/redo hooks to the edit menu.
    mainMenu.editMenu.undoers.redo.add({
        id: CommandIDs.redo,
        isEnabled
    });
    mainMenu.editMenu.undoers.undo.add({
        id: CommandIDs.undo,
        isEnabled
    });
    // Add a clearer to the edit menu
    mainMenu.editMenu.clearers.clearAll.add({
        id: CommandIDs.clearAllOutputs,
        isEnabled
    });
    mainMenu.editMenu.clearers.clearCurrent.add({
        id: CommandIDs.clearOutputs,
        isEnabled
    });
    // Add a console creator the the Kernel menu
    mainMenu.fileMenu.consoleCreators.add({
        id: CommandIDs.createConsole,
        isEnabled
    });
    // Add a close and shutdown command to the file menu.
    mainMenu.fileMenu.closeAndCleaners.add({
        id: CommandIDs.closeAndShutdown,
        isEnabled
    });
    // Add a kernel user to the Kernel menu
    mainMenu.kernelMenu.kernelUsers.changeKernel.add({
        id: CommandIDs.changeKernel,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.clearWidget.add({
        id: CommandIDs.clearAllOutputs,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.interruptKernel.add({
        id: CommandIDs.interrupt,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.reconnectToKernel.add({
        id: CommandIDs.reconnectToKernel,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.restartKernel.add({
        id: CommandIDs.restart,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.shutdownKernel.add({
        id: CommandIDs.shutdown,
        isEnabled
    });
    // Add an IEditorViewer to the application view menu
    mainMenu.viewMenu.editorViewers.toggleLineNumbers.add({
        id: CommandIDs.toggleAllLines,
        isEnabled
    });
    // Add an ICodeRunner to the application run menu
    mainMenu.runMenu.codeRunners.restart.add({
        id: CommandIDs.restart,
        isEnabled
    });
    mainMenu.runMenu.codeRunners.run.add({
        id: CommandIDs.runAndAdvance,
        isEnabled
    });
    mainMenu.runMenu.codeRunners.runAll.add({ id: CommandIDs.runAll, isEnabled });
    // Add kernel information to the application help menu.
    mainMenu.helpMenu.getKernel.add({
        id: CommandIDs.getKernel,
        isEnabled
    });
}
/**
 * A namespace for module private functionality.
 */
var Private;
(function (Private) {
    /**
     * Create a console connected with a notebook kernel
     *
     * @param commands Commands registry
     * @param widget Notebook panel
     * @param activate Should the console be activated
     */
    function createConsole(commands, widget, activate) {
        const options = {
            path: widget.context.path,
            preferredLanguage: widget.context.model.defaultKernelLanguage,
            activate: activate,
            ref: widget.id,
            insertMode: 'split-bottom',
            type: 'Linked Console'
        };
        return commands.execute('console:create', options);
    }
    Private.createConsole = createConsole;
    /**
     * Whether there is an active notebook.
     */
    function isEnabled(shell, tracker) {
        return (tracker.currentWidget !== null &&
            tracker.currentWidget === shell.currentWidget);
    }
    Private.isEnabled = isEnabled;
    /**
     * Whether there is an notebook active, with a single selected cell.
     */
    function isEnabledAndSingleSelected(shell, tracker) {
        if (!Private.isEnabled(shell, tracker)) {
            return false;
        }
        const { content } = tracker.currentWidget;
        const index = content.activeCellIndex;
        // If there are selections that are not the active cell,
        // this command is confusing, so disable it.
        for (let i = 0; i < content.widgets.length; ++i) {
            if (content.isSelected(content.widgets[i]) && i !== index) {
                return false;
            }
        }
        return true;
    }
    Private.isEnabledAndSingleSelected = isEnabledAndSingleSelected;
    /**
     * Whether there is an notebook active, with a single selected cell.
     */
    function isEnabledAndHeadingSelected(shell, tracker) {
        if (!Private.isEnabled(shell, tracker)) {
            return false;
        }
        const { content } = tracker.currentWidget;
        const index = content.activeCellIndex;
        if (!(content.activeCell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.MarkdownCell)) {
            return false;
        }
        // If there are selections that are not the active cell,
        // this command is confusing, so disable it.
        for (let i = 0; i < content.widgets.length; ++i) {
            if (content.isSelected(content.widgets[i]) && i !== index) {
                return false;
            }
        }
        return true;
    }
    Private.isEnabledAndHeadingSelected = isEnabledAndHeadingSelected;
    /**
     * The default Export To ... formats and their human readable labels.
     */
    function getFormatLabels(translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.nullTranslator;
        const trans = translator.load('jupyterlab');
        return {
            html: trans.__('HTML'),
            latex: trans.__('LaTeX'),
            markdown: trans.__('Markdown'),
            pdf: trans.__('PDF'),
            rst: trans.__('ReStructured Text'),
            script: trans.__('Executable Script'),
            slides: trans.__('Reveal.js Slides')
        };
    }
    Private.getFormatLabels = getFormatLabels;
    /**
     * Raises a silent notification that is read by screen readers
     *
     * FIXME: Once a notificatiom API is introduced (https://github.com/jupyterlab/jupyterlab/issues/689),
     * this can be refactored to use the same.
     *
     * More discussion at https://github.com/jupyterlab/jupyterlab/pull/9031#issuecomment-773541469
     *
     *
     * @param message Message to be relayed to screen readers
     * @param notebookNode DOM node to which the notification container is attached
     */
    function raiseSilentNotification(message, notebookNode) {
        const hiddenAlertContainerId = `sr-message-container-${notebookNode.id}`;
        const hiddenAlertContainer = document.getElementById(hiddenAlertContainerId) ||
            document.createElement('div');
        // If the container is not available, append the newly created container
        // to the current notebook panel and set related properties
        if (hiddenAlertContainer.getAttribute('id') !== hiddenAlertContainerId) {
            hiddenAlertContainer.classList.add('sr-only');
            hiddenAlertContainer.setAttribute('id', hiddenAlertContainerId);
            hiddenAlertContainer.setAttribute('role', 'alert');
            hiddenAlertContainer.hidden = true;
            notebookNode.appendChild(hiddenAlertContainer);
        }
        // Insert/Update alert container with the notification message
        hiddenAlertContainer.innerText = message;
    }
    Private.raiseSilentNotification = raiseSilentNotification;
    /**
     * A widget hosting a cloned output area.
     */
    class ClonedOutputArea extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_18__.Panel {
        constructor(options) {
            super();
            this._cell = null;
            const trans = (options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.nullTranslator).load('jupyterlab');
            this._notebook = options.notebook;
            this._index = options.index !== undefined ? options.index : -1;
            this._cell = options.cell || null;
            this.id = `LinkedOutputView-${_lumino_coreutils__WEBPACK_IMPORTED_MODULE_16__.UUID.uuid4()}`;
            this.title.label = 'Output View';
            this.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_14__.notebookIcon;
            this.title.caption = this._notebook.title.label
                ? trans.__('For Notebook: %1', this._notebook.title.label)
                : trans.__('For Notebook:');
            this.addClass('jp-LinkedOutputView');
            // Wait for the notebook to be loaded before
            // cloning the output area.
            void this._notebook.context.ready.then(() => {
                if (!this._cell) {
                    this._cell = this._notebook.content.widgets[this._index];
                }
                if (!this._cell || this._cell.model.type !== 'code') {
                    this.dispose();
                    return;
                }
                const clone = this._cell.cloneOutputArea();
                this.addWidget(clone);
            });
        }
        /**
         * The index of the cell in the notebook.
         */
        get index() {
            return this._cell
                ? _lumino_algorithm__WEBPACK_IMPORTED_MODULE_15__.ArrayExt.findFirstIndex(this._notebook.content.widgets, c => c === this._cell)
                : this._index;
        }
        /**
         * The path of the notebook for the cloned output area.
         */
        get path() {
            return this._notebook.context.path;
        }
    }
    Private.ClonedOutputArea = ClonedOutputArea;
})(Private || (Private = {}));


/***/ }),

/***/ "./style/tag.svg":
/*!***********************!*\
  !*** ./style/tag.svg ***!
  \***********************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 448 512\">\n  <!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.-->\n  <path d=\"M0 80L0 229.5c0 17 6.7 33.3 18.7 45.3l176 176c25 25 65.5 25 90.5 0L418.7 317.3c25-25 25-65.5 0-90.5l-176-176c-12-12-28.3-18.7-45.3-18.7L48 32C21.5 32 0 53.5 0 80zm112 32a32 32 0 1 1 0 64 32 32 0 1 1 0-64z\" class=\"jp-icon3 tag-icon\" stroke=\"#616161\" stroke-width=\"50\"></path>\n</svg>";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.ed29adaa627534f5d2d3.js.map