// import { createStore } from "redux";
// import { produce } from "immer";
// import { aUserUploadedFiles } from "@/actions/files";

// // state
// const initialState = {
//   pattern: '',
//   isLoading: false,
//   files: [],
//   token: null,
// };

// // actions creators

// export const loadStateChange = () => ({ type: "loadStateChange" });

// export const loadFiles = async (token, pattern) => ({
//     type: "loadFiles",
//     payload: { files: [await aUserUploadedFiles(token, pattern)][0] }
// })

// export const patternChange = (pattern) => ({
//   type: "patternChange",
//   payload: { pattern: pattern  },
// });

// export const tokenObtained = (token) => ({
//     type: "tokenObtained",
//     payload: { token: token },
//   });

// function reducer(state = initialState, action) {
//   if (action.type === "loadStateChange") {
//     return produce(state, (draft) => {
//       draft.isLoading = !draft.isLoading;
//     });
//   }
//   if (action.type === "patternChange") {
//     return produce(state, (draft) => {
//         draft.pattern = action.payload.pattern;;
//         draft.files = action.payload.files;
//     })
//   }
//   if (action.type === "tokenObtained") {
//     return produce(state, (draft) => {
//         draft.token = action.payload.token;
//     })
//   }
//   if (action.type === "loadFiles") {
//     return produce(state, (draft) => {
//         draft.files = action.payload.files;
//     })
//   }
//   return state;
// }

// export const store = createStore(reducer);

// store.subscribe(() => {
//     console.log("Nouveau state:");
//     console.log(store.getState());
//   }
// );
