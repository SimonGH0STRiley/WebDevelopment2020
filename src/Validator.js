import {helpers} from "vuelidate/lib/validators";

export const passwordRule = helpers.regex('password', /^(?=.*[a-z])(?=.*[A-Z])((?=.*\d){2,})[a-zA-Z\d]{6,}$/);
export const identityNumberRule = helpers.regex('mainlandID', /^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/);
export const militaryIDRule = helpers.regex('militaryID', /^[\u4E00-\u9FA5](字第)([0-9a-zA-Z]{4,8})(号?)$/);
export const passportRule = helpers.regex('passportID', /^1[45][0-9]{7}|([PS]\d{7})|([SG]\d{8})|([GTSLQDAF]\d{8})$/);
export const HKMCIDRule = helpers.regex('HongKongMacaoID', /^[HM]\d{10}$/);
export const TWIDRule = helpers.regex('TaiwanID', /^[0-9]{10}$/);
export const phoneRule = helpers.regex('phoneNumber',/^(13[0-9]|14[5-9]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{08}$/)
export const cityRule = helpers.regex('chineseCityName', /^[\u4e00-\u9fa5]{1,10}$/)

