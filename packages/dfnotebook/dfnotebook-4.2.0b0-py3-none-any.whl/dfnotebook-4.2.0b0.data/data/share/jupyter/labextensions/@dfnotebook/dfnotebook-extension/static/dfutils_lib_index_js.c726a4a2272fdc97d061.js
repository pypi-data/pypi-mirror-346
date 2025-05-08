"use strict";
(self["webpackChunk_dfnotebook_dfnotebook_extension"] = self["webpackChunk_dfnotebook_dfnotebook_extension"] || []).push([["dfutils_lib_index_js"],{

/***/ "../dfutils/lib/index.js":
/*!*******************************!*\
  !*** ../dfutils/lib/index.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   cellIdIntToStr: () => (/* binding */ cellIdIntToStr),
/* harmony export */   cellIdStrToInt: () => (/* binding */ cellIdStrToInt),
/* harmony export */   truncateCellId: () => (/* binding */ truncateCellId)
/* harmony export */ });
function cellIdIntToStr(id) {
    return id.toString(16).padStart(8, '0');
}
function cellIdStrToInt(id) {
    return parseInt(id, 16);
}
function truncateCellId(id) {
    return id.replace(/-/g, '').substring(0, 8);
}


/***/ })

}]);
//# sourceMappingURL=dfutils_lib_index_js.c726a4a2272fdc97d061.js.map