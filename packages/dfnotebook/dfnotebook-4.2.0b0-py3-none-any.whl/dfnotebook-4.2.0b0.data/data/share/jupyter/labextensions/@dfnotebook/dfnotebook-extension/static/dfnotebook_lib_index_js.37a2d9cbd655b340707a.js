"use strict";
(self["webpackChunk_dfnotebook_dfnotebook_extension"] = self["webpackChunk_dfnotebook_dfnotebook_extension"] || []).push([["dfnotebook_lib_index_js"],{

/***/ "../dfnotebook/lib/cellexecutor.js":
/*!*****************************************!*\
  !*** ../dfnotebook/lib/cellexecutor.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   dfCommGetData: () => (/* binding */ dfCommGetData),
/* harmony export */   getAllTags: () => (/* binding */ getAllTags),
/* harmony export */   getCellsMetadata: () => (/* binding */ getCellsMetadata),
/* harmony export */   runCell: () => (/* binding */ runCell)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @dfnotebook/dfcells */ "webpack/sharing/consume/default/@dfnotebook/dfcells/@dfnotebook/dfcells");
/* harmony import */ var _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./model */ "../dfnotebook/lib/model.js");
/* harmony import */ var _dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @dfnotebook/dfutils */ "webpack/sharing/consume/default/@dfnotebook/dfutils/@dfnotebook/dfutils");
/* harmony import */ var _dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_6__);









/**
 * Run a single notebook cell.
 *
 * @param options Cell execution options
 * @returns Execution status
 */
async function runCell({ cell, notebook, notebookConfig, onCellExecuted, onCellExecutionScheduled, sessionContext, sessionDialogs, translator }) {
    var _a, _b;
    translator = translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
    const trans = translator.load('jupyterlab');
    const notebookId = (0,_dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_5__.getNotebookId)(cell);
    switch (cell.model.type) {
        case 'markdown':
            cell.rendered = true;
            cell.inputHidden = false;
            onCellExecuted({ cell, success: true });
            break;
        case 'code':
            if (sessionContext) {
                if (sessionContext.isTerminating) {
                    await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                        title: trans.__('Kernel Terminating'),
                        body: trans.__('The kernel for %1 appears to be terminating. You can not run any cell for now.', (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.path),
                        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]
                    });
                    break;
                }
                if (sessionContext.pendingInput) {
                    await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                        title: trans.__('Cell not executed due to pending input'),
                        body: trans.__('The cell has not been executed to avoid kernel deadlock as there is another pending input! Submit your pending input and try again.'),
                        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]
                    });
                    return false;
                }
                if (sessionContext.hasNoKernel) {
                    const shouldSelect = await sessionContext.startKernel();
                    if (shouldSelect && sessionDialogs) {
                        await sessionDialogs.selectKernel(sessionContext);
                    }
                }
                if (sessionContext.hasNoKernel) {
                    cell.model.sharedModel.transact(() => {
                        cell.model.clearExecution();
                    });
                    return true;
                }
                const deletedCells = notebook.deletedCells;
                onCellExecutionScheduled({ cell });
                let ran = false;
                try {
                    let reply;
                    // !!! DATAFLOW NOTEBOOK CODE !!!
                    if (notebook instanceof _model__WEBPACK_IMPORTED_MODULE_7__.DataflowNotebookModel) {
                        const cellUUID = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_6__.truncateCellId)(cell.model.id);
                        let dfData = getCellsMetadata(notebook, cellUUID);
                        if (!notebook.getMetadata('enable_tags')) {
                            dfData.dfMetadata.input_tags = {};
                        }
                        reply = await _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_5__.DataflowCodeCell.execute(cell, sessionContext, {
                            deletedCells,
                            recordTiming: notebookConfig.recordTiming
                        }, dfData.dfMetadata, dfData.cellIdModelMap);
                        resetCellPrompt(notebook, cell);
                        if (reply) {
                            await updateDataflowMetadata(notebook, reply, notebookId);
                        }
                        if ((_b = sessionContext === null || sessionContext === void 0 ? void 0 : sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel) {
                            await dfCommPostData(notebookId, notebook, sessionContext);
                        }
                    }
                    else {
                        reply = await _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell.execute(cell, sessionContext, {
                            deletedCells,
                            recordTiming: notebookConfig.recordTiming
                        });
                    }
                    // !!! END DATAFLOW NOTEBOOK CODE !!!
                    deletedCells.splice(0, deletedCells.length);
                    ran = (() => {
                        if (cell.isDisposed) {
                            return false;
                        }
                        if (!reply) {
                            return true;
                        }
                        if (reply.content.status === 'ok') {
                            const content = reply.content;
                            if (content.payload && content.payload.length) {
                                handlePayload(content, notebook, cell);
                            }
                            return true;
                        }
                        else {
                            throw new _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__.KernelError(reply.content);
                        }
                    })();
                }
                catch (reason) {
                    if (cell.isDisposed || reason.message.startsWith('Canceled')) {
                        ran = false;
                    }
                    else {
                        onCellExecuted({
                            cell,
                            success: false,
                            error: reason
                        });
                        throw reason;
                    }
                }
                if (ran) {
                    onCellExecuted({ cell, success: true });
                }
                return ran;
            }
            cell.model.sharedModel.transact(() => {
                cell.model.clearExecution();
            }, false);
            break;
        default:
            break;
    }
    return Promise.resolve(true);
}
async function dfCommPostData(notebookId, notebook, sessionContext) {
    const dfData = getCellsMetadata(notebook, '');
    if (!notebook.getMetadata('enable_tags')) {
        dfData.dfMetadata.input_tags = {};
    }
    try {
        const response = await dfCommGetData(sessionContext, { 'dfMetadata': dfData.dfMetadata });
        if ((response === null || response === void 0 ? void 0 : response.code_dict) && Object.keys(response.code_dict).length > 0) {
            await updateNotebookCells(notebook, notebookId, response.code_dict);
        }
    }
    catch (error) {
        console.error('Error during kernel communication:', error);
    }
}
async function dfCommGetData(sessionContext, commData) {
    return new Promise((resolve) => {
        var _a, _b;
        const comm = (_b = (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.createComm('dfcode');
        if (!comm) {
            resolve();
            return;
        }
        comm.open();
        comm.send(commData);
        comm.onMsg = (msg) => {
            const content = msg.content.data;
            resolve(content);
        };
    });
}
async function updateNotebookCells(notebook, notebookId, codeDict) {
    const cellMap = notebookId ? _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_5__.notebookCellMap.get(notebookId) : undefined;
    const cellsArray = Array.from(notebook.cells);
    cellsArray.forEach(cell => {
        if (cell.type === 'code') {
            const cId = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_6__.truncateCellId)(cell.id);
            if (codeDict.hasOwnProperty(cId)) {
                const updatedCode = codeDict[cId];
                const dfmetadata = cell.getMetadata('dfmetadata');
                if (cellMap) {
                    if ((cellMap === null || cellMap === void 0 ? void 0 : cellMap.get(cId)) !== cell.sharedModel.getSource()) {
                        cell.sharedModel.setSource(updatedCode);
                        cellMap.set(cId, updatedCode.trim());
                    }
                    else {
                        cellMap.set(cId, updatedCode.trim());
                        cell.sharedModel.setSource(updatedCode);
                    }
                }
                cell.setMetadata('dfmetadata', dfmetadata);
            }
        }
    });
}
async function updateDataflowMetadata(notebook, reply, notebookId) {
    const content = reply === null || reply === void 0 ? void 0 : reply.content;
    if (!content)
        return;
    const cellMap = notebookId ? _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_5__.notebookCellMap.get(notebookId) : undefined;
    const allTags = getAllTags(notebook);
    const cellsArray = Array.from(notebook.cells);
    cellsArray.forEach((cell, index) => {
        if (cell.type === 'code') {
            updateCellMetadata(cell, content, allTags, cellMap);
        }
    });
}
function updateCellMetadata(cellModel, content, allTags, cellMap) {
    var _a, _b;
    const cId = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_6__.truncateCellId)(cellModel.id);
    const dfmetadata = cellModel.getMetadata('dfmetadata') || {};
    if ((_a = content.persistent_code) === null || _a === void 0 ? void 0 : _a[cId]) {
        dfmetadata.persistentCode = content.persistent_code[cId];
    }
    if ((_b = content.identifier_refs) === null || _b === void 0 ? void 0 : _b[cId]) {
        const refs = content.identifier_refs[cId];
        dfmetadata.inputVars = {
            ref: refs,
            tag_refs: mapTagsToRefs(refs, allTags)
        };
        let cellOutputTags = [];
        for (let i = 0; i < cellModel.outputs.length; ++i) {
            const out = cellModel.outputs.get(i);
            if (out.metadata['output_tag']) {
                cellOutputTags.push(out.metadata['output_tag']);
            }
        }
        dfmetadata.outputVars = cellOutputTags;
        if (cellMap) {
            cellMap.set(cId, cellModel.sharedModel.getSource());
        }
    }
    cellModel.setMetadata('dfmetadata', dfmetadata);
}
function mapTagsToRefs(refs, allTags) {
    const tagRefs = {};
    Object.keys(refs).forEach(key => {
        if (allTags[key]) {
            tagRefs[key] = allTags[key];
        }
    });
    return tagRefs;
}
function resetCellPrompt(notebook, cell) {
    var _a, _b;
    const currInputArea = cell.inputArea;
    const dfmetadata = (_a = cell.model) === null || _a === void 0 ? void 0 : _a.getMetadata('dfmetadata');
    const currTag = dfmetadata.tag;
    if (currInputArea) {
        if (!notebook.getMetadata('enable_tags')) {
            currInputArea.addTag("");
            (_b = cell.model) === null || _b === void 0 ? void 0 : _b.setMetadata('dfmetadata', dfmetadata);
        }
        else {
            currInputArea.addTag(currTag);
        }
    }
}
function getAllTags(notebook) {
    const allTags = {};
    const cellsArray = Array.from(notebook.cells);
    cellsArray.forEach(cell => {
        if (cell.type === 'code') {
            const dfmetadata = cell.getMetadata('dfmetadata');
            const tag = dfmetadata === null || dfmetadata === void 0 ? void 0 : dfmetadata.tag;
            if (tag) {
                const cId = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_6__.truncateCellId)(cell.id);
                allTags[cId] = tag;
            }
        }
    });
    return allTags;
}
function getCellsMetadata(notebook, cellUUID) {
    const codeDict = {};
    const cellIdModelMap = {};
    const outputTags = {};
    const inputTags = {};
    const allRefs = {};
    const cellsArray = Array.from(notebook.cells);
    cellsArray.forEach(cell => {
        if (cell.type === 'code') {
            const c = cell;
            const cId = (0,_dfnotebook_dfutils__WEBPACK_IMPORTED_MODULE_6__.truncateCellId)(c.id);
            const dfmetadata = c.getMetadata('dfmetadata');
            if (!dfmetadata.persistentCode) {
                cellIdModelMap[cId] = c;
                return;
            }
            const inputTag = dfmetadata === null || dfmetadata === void 0 ? void 0 : dfmetadata.tag;
            if (inputTag) {
                inputTags[inputTag] = cId;
            }
            codeDict[cId] = c.sharedModel.getSource();
            cellIdModelMap[cId] = c;
            outputTags[cId] = dfmetadata.outputVars;
            allRefs[cId] = dfmetadata.inputVars;
        }
    });
    const dfMetadata = {
        // FIXME replace with utility function (see dfcells/widget)
        uuid: cellUUID,
        code_dict: codeDict,
        output_tags: outputTags,
        input_tags: inputTags,
        auto_update_flags: {},
        force_cached_flags: {},
        all_refs: allRefs,
        executed_code: {}
    };
    return { dfMetadata, cellIdModelMap };
}
/**
 * Handle payloads from an execute reply.
 *
 * #### Notes
 * Payloads are deprecated and there are no official interfaces for them in
 * the kernel type definitions.
 * See [Payloads (DEPRECATED)](https://jupyter-client.readthedocs.io/en/latest/messaging.html#payloads-deprecated).
 */
function handlePayload(content, notebook, cell) {
    var _a;
    const setNextInput = (_a = content.payload) === null || _a === void 0 ? void 0 : _a.filter(i => {
        return i.source === 'set_next_input';
    })[0];
    if (!setNextInput) {
        return;
    }
    const text = setNextInput.text;
    const replace = setNextInput.replace;
    if (replace) {
        cell.model.sharedModel.setSource(text);
        return;
    }
    // Create a new code cell and add as the next cell.
    const notebookModel = notebook.sharedModel;
    const cells = notebook.cells;
    const index = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.findIndex)(cells, model => model === cell.model);
    // While this cell has no outputs and could be trusted following the letter
    // of Jupyter trust model, its content comes from kernel and hence is not
    // necessarily controlled by the user; if we set it as trusted, a user
    // executing cells in succession could end up with unwanted trusted output.
    if (index === -1) {
        notebookModel.insertCell(notebookModel.cells.length, {
            cell_type: 'code',
            source: text,
            metadata: {
                trusted: false
            }
        });
    }
    else {
        notebookModel.insertCell(index + 1, {
            cell_type: 'code',
            source: text,
            metadata: {
                trusted: false
            }
        });
    }
}


/***/ }),

/***/ "../dfnotebook/lib/index.js":
/*!**********************************!*\
  !*** ../dfnotebook/lib/index.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DataflowNotebook: () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_4__.DataflowNotebook),
/* harmony export */   DataflowNotebookModel: () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_1__.DataflowNotebookModel),
/* harmony export */   DataflowNotebookModelFactory: () => (/* reexport safe */ _modelfactory__WEBPACK_IMPORTED_MODULE_2__.DataflowNotebookModelFactory),
/* harmony export */   DataflowNotebookPanel: () => (/* reexport safe */ _panel__WEBPACK_IMPORTED_MODULE_3__.DataflowNotebookPanel),
/* harmony export */   DataflowNotebookWidgetFactory: () => (/* reexport safe */ _widgetfactory__WEBPACK_IMPORTED_MODULE_6__.DataflowNotebookWidgetFactory),
/* harmony export */   DataflowStaticNotebook: () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_4__.DataflowStaticNotebook),
/* harmony export */   IDataflowNotebookWidgetFactory: () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_5__.IDataflowNotebookWidgetFactory),
/* harmony export */   dfCommGetData: () => (/* reexport safe */ _cellexecutor__WEBPACK_IMPORTED_MODULE_0__.dfCommGetData),
/* harmony export */   getAllTags: () => (/* reexport safe */ _cellexecutor__WEBPACK_IMPORTED_MODULE_0__.getAllTags),
/* harmony export */   getCellsMetadata: () => (/* reexport safe */ _cellexecutor__WEBPACK_IMPORTED_MODULE_0__.getCellsMetadata),
/* harmony export */   runCell: () => (/* reexport safe */ _cellexecutor__WEBPACK_IMPORTED_MODULE_0__.runCell)
/* harmony export */ });
/* harmony import */ var _cellexecutor__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./cellexecutor */ "../dfnotebook/lib/cellexecutor.js");
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./model */ "../dfnotebook/lib/model.js");
/* harmony import */ var _modelfactory__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./modelfactory */ "../dfnotebook/lib/modelfactory.js");
/* harmony import */ var _panel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./panel */ "../dfnotebook/lib/panel.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./widget */ "../dfnotebook/lib/widget.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tokens */ "../dfnotebook/lib/tokens.js");
/* harmony import */ var _widgetfactory__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widgetfactory */ "../dfnotebook/lib/widgetfactory.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module dfnotebook
 */









/***/ }),

/***/ "../dfnotebook/lib/model.js":
/*!**********************************!*\
  !*** ../dfnotebook/lib/model.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DataflowNotebookModel: () => (/* binding */ DataflowNotebookModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

class DataflowNotebookModel extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookModel {
    fromJSON(value) {
        var _a, _b;
        let isDataflow = true;
        if (((_b = (_a = value.metadata) === null || _a === void 0 ? void 0 : _a.kernelspec) === null || _b === void 0 ? void 0 : _b.name) && value.metadata.kernelspec.name != 'dfpython3') {
            isDataflow = false;
        }
        super.fromJSON(value);
        this.setMetadata('dfnotebook', isDataflow);
        this.setMetadata('enable_tags', true);
    }
}


/***/ }),

/***/ "../dfnotebook/lib/modelfactory.js":
/*!*****************************************!*\
  !*** ../dfnotebook/lib/modelfactory.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DataflowNotebookModelFactory: () => (/* binding */ DataflowNotebookModelFactory)
/* harmony export */ });
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./model */ "../dfnotebook/lib/model.js");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A model factory for notebooks.
 */
class DataflowNotebookModelFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookModelFactory {
    /**
     * Create a new model for a given path.
     *
     * @param languagePreference - An optional kernel language preference.
     *
     * @returns A new document model.
     */
    createNew(options = {}) {
        return new _model__WEBPACK_IMPORTED_MODULE_1__.DataflowNotebookModel({
            languagePreference: options.languagePreference,
            sharedModel: options.sharedModel,
            collaborationEnabled: options.collaborationEnabled && this.collaborative,
            //@ts-ignore
            disableDocumentWideUndoRedo: this._disableDocumentWideUndoRedo
        });
    }
    /**
     * The name of the model.
     */
    get name() {
        return 'dfnotebook';
    }
}


/***/ }),

/***/ "../dfnotebook/lib/panel.js":
/*!**********************************!*\
  !*** ../dfnotebook/lib/panel.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DataflowNotebookPanel: () => (/* binding */ DataflowNotebookPanel)
/* harmony export */ });
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../dfnotebook/lib/widget.js");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A namespace for `DataflowNotebookPanel` statics.
 */
var DataflowNotebookPanel;
(function (DataflowNotebookPanel) {
    /**
     * The default implementation of an `IContentFactory`.
     */
    class ContentFactory extends _widget__WEBPACK_IMPORTED_MODULE_1__.DataflowNotebook.ContentFactory {
        /**
         * Create a new content area for the panel.
         */
        createNotebook(options) {
            return new _widget__WEBPACK_IMPORTED_MODULE_1__.DataflowNotebook(options);
        }
    }
    DataflowNotebookPanel.ContentFactory = ContentFactory;
    /**
     * The notebook renderer token.
     */
    DataflowNotebookPanel.IContentFactory = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@dfnotebook/dfnotebook:IContentFactory', `A factory object that creates new dataflow notebooks.
    Use this if you want to create and host dataflow notebooks in your own UI elements.`);
})(DataflowNotebookPanel || (DataflowNotebookPanel = {}));


/***/ }),

/***/ "../dfnotebook/lib/tokens.js":
/*!***********************************!*\
  !*** ../dfnotebook/lib/tokens.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IDataflowNotebookWidgetFactory: () => (/* binding */ IDataflowNotebookWidgetFactory)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The dfnotebook widget factory token.
 */
const IDataflowNotebookWidgetFactory = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@dfnotebook/dfnotebook:DataflowNotebookWidgetFactory', 'A service to create the dataflow notebook viewer.');


/***/ }),

/***/ "../dfnotebook/lib/widget.js":
/*!***********************************!*\
  !*** ../dfnotebook/lib/widget.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DataflowNotebook: () => (/* binding */ DataflowNotebook),
/* harmony export */   DataflowStaticNotebook: () => (/* binding */ DataflowStaticNotebook)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @dfnotebook/dfcells */ "webpack/sharing/consume/default/@dfnotebook/dfcells/@dfnotebook/dfcells");
/* harmony import */ var _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * The namespace for the `StaticNotebook` class statics.
 */
var DataflowStaticNotebook;
(function (DataflowStaticNotebook) {
    /**
     * The default implementation of an `IContentFactory`.
     */
    class ContentFactory extends _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_1__.DataflowCell.ContentFactory {
        /**
         * Create a new code cell widget.
         *
         * #### Notes
         * If no cell content factory is passed in with the options, the one on the
         * notebook content factory is used.
         */
        createCodeCell(options) {
            if (!options.contentFactory) {
                options.contentFactory = this;
            }
            return new _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_1__.DataflowCodeCell(options).initializeState();
        }
        /**
         * Create a new markdown cell widget.
         *
         * #### Notes
         * If no cell content factory is passed in with the options, the one on the
         * notebook content factory is used.
         */
        createMarkdownCell(options) {
            if (!options.contentFactory) {
                options.contentFactory = this;
            }
            return new _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_1__.DataflowMarkdownCell(options).initializeState();
        }
        /**
         * Create a new raw cell widget.
         *
         * #### Notes
         * If no cell content factory is passed in with the options, the one on the
         * notebook content factory is used.
         */
        createRawCell(options) {
            if (!options.contentFactory) {
                options.contentFactory = this;
            }
            return new _dfnotebook_dfcells__WEBPACK_IMPORTED_MODULE_1__.DataflowRawCell(options).initializeState();
        }
    }
    DataflowStaticNotebook.ContentFactory = ContentFactory;
})(DataflowStaticNotebook || (DataflowStaticNotebook = {}));
class DataflowNotebook extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.Notebook {
}
(function (DataflowNotebook) {
    /**
     * The default implementation of a notebook content factory..
     *
     * #### Notes
     * Override methods on this class to customize the default notebook factory
     * methods that create notebook content.
     */
    class ContentFactory extends DataflowStaticNotebook.ContentFactory {
    }
    DataflowNotebook.ContentFactory = ContentFactory;
})(DataflowNotebook || (DataflowNotebook = {}));


/***/ }),

/***/ "../dfnotebook/lib/widgetfactory.js":
/*!******************************************!*\
  !*** ../dfnotebook/lib/widgetfactory.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DataflowNotebookWidgetFactory: () => (/* binding */ DataflowNotebookWidgetFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
// import { DocumentRegistry } from "@jupyterlab/docregistry";

/**
 * A widget factory for notebook panels.
 */
class DataflowNotebookWidgetFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookWidgetFactory {
}


/***/ })

}]);
//# sourceMappingURL=dfnotebook_lib_index_js.37a2d9cbd655b340707a.js.map