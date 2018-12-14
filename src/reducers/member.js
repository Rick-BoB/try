import Store from "../store/member";

export const initialState = Store;

export default function userReducer(state = initialState, action) {
  switch (action.type) {
    case "USER_LOGIN": {
      if (action.data) {
        return {
          ...state,
          loading: false,
          error: null,
          uid: action.data.uid,
          email: action.data.email,
          emailVerified: action.data.emailVerified
        };
      }
      return initialState;
    }
    case "USER_DETAILS_UPDATE": {
      if (action.data && action.dataSeller) {
        return {
          ...state,
          loading: false,
          error: null,
          firstName: action.data.firstName,
          lastName: action.data.lastName,
          cellphone: action.data.phoneNumber,
          createdAt: action.dataSeller.created_at,
          signedUp: action.data.signedUp,
          role: action.data.role,
          code: action.dataSeller.code,
          commission: action.dataSeller.commission,
          orders: action.dataOrders,
          referrals: action.dataReferrals,
          validOrders: action.dataValidOrders,
          clients: action.dataClients
        };
      }
      return initialState;
    }
    case "USER_ERROR": {
      if (action.data) {
        return {
          ...state,
          loading: false,
          error: action.data
        };
      }
      return initialState;
    }
    case "USER_RESET": {
      return initialState;
    }
    default:
      return state;
  }
}